import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from test_translation_helpers import REPO, config

from translation_pipeline.checks import compare_translation
from translation_pipeline.frontmatter import add_modification_notice, split_document
from translation_pipeline.protect import Protector, fenced_blocks, prose_only, protected_inventory
from translation_pipeline.segment import heading_levels
from translation_pipeline.source_errata import ERRATA_PATH, apply_source_errata, load_errata
from translation_pipeline.terms import TermRules

LDAP = "_security/authentication-backends/ldap.md"
KEY_VALUE = "_data-prepper/pipelines/configuration/processors/key-value.md"
REPLACE = "_sql-and-ppl/ppl/commands/replace.md"


def source(page):
    return (REPO / config.SOURCE_STORE_DIR / page).read_bytes().decode("utf-8")


def sha(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def headings(text):
    return heading_levels(Protector().protect_body(text))


class SourceErrataFileTests(unittest.TestCase):
    def test_every_erratum_is_pinned_to_its_immutable_baseline(self):
        data = json.loads(ERRATA_PATH.read_text(encoding="utf-8"))
        inventory = json.loads((REPO / config.SOURCE_INVENTORY_PATH).read_text(encoding="utf-8"))["pages"]
        self.assertEqual(set(data["errata"]), set(load_errata()))
        for digest, entry in data["errata"].items():
            text = source(entry["page"])
            self.assertEqual(sha(text), digest, entry["page"])
            self.assertEqual(inventory[entry["page"]], digest, entry["page"])
            self.assertTrue(entry["reason"])
            repaired = apply_source_errata(text)
            self.assertNotEqual(repaired, text)
            # Applying again is a no-op: the repaired text has another hash.
            self.assertEqual(apply_source_errata(repaired), repaired)
            # Undoing the replacements restores the baseline byte for byte, so
            # nothing else (code, API literals, front matter) was touched.
            undone = repaired
            for item in reversed(entry["replacements"]):
                self.assertEqual(undone.count(item["after"]), 1)
                undone = undone.replace(item["after"], item["before"], 1)
            self.assertEqual(undone, text)
            self.assertEqual(split_document(repaired).raw, split_document(text).raw)

    def test_sha_pin_leaves_changed_or_unrelated_input_alone(self):
        text = source(LDAP)
        for other in (text + "\n", text.replace("Timeouts", "Time-outs", 1), text.replace("\n", "\r\n")):
            self.assertEqual(apply_source_errata(other), other)
        unrelated = "  follow_referrals: false\n\nAdd this setting to the LDAP section.\n"
        self.assertEqual(apply_source_errata(unrelated), unrelated)
        self.assertEqual(apply_source_errata(source("_security/authentication-backends/openid-connect.md")),
                         source("_security/authentication-backends/openid-connect.md"))

    def test_before_pattern_must_occur_exactly_once(self):
        with tempfile.TemporaryDirectory() as tmp:
            for text in ("x y", "x x y"):
                path = Path(tmp) / f"errata-{len(text)}.json"
                path.write_text(json.dumps({"schema_version": 1, "errata": {sha(text): {
                    "page": "p.md", "reason": "test",
                    "replacements": [{"before": "x", "after": "z"}]}}}), encoding="utf-8")
                if text == "x y":
                    self.assertEqual(apply_source_errata(text, path), "z y")
                else:
                    with self.assertRaisesRegex(ValueError, "2 times"):
                        apply_source_errata(text, path)
            missing = "a b"
            path = Path(tmp) / "errata-missing.json"
            path.write_text(json.dumps({"schema_version": 1, "errata": {sha(missing): {
                "page": "p.md", "reason": "test", "replacements": [{"before": "x", "after": "z"}]}}}),
                encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "0 times"):
                apply_source_errata(missing, path)

    def test_malformed_errata_file_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            bad_entries = [
                {"NOTAHASH": {"reason": "r", "replacements": [{"before": "a", "after": "b"}]}},
                {sha("t"): {"reason": "", "replacements": [{"before": "a", "after": "b"}]}},
                {sha("t"): {"reason": "r", "replacements": []}},
                {sha("t"): {"reason": "r", "replacements": [{"before": "", "after": "b"}]}},
                {sha("t"): {"reason": "r", "replacements": [{"before": "a", "after": "a"}]}},
            ]
            for i, errata in enumerate(bad_entries):
                path = Path(tmp) / f"bad-{i}.json"
                path.write_text(json.dumps({"schema_version": 1, "errata": errata}), encoding="utf-8")
                with self.assertRaises(ValueError, msg=errata):
                    apply_source_errata("t", path)


class SourceErrataRepairTests(unittest.TestCase):
    def test_ldap_closing_fence_exposes_prose_and_timeouts_heading(self):
        text = source(LDAP)
        repaired = apply_source_errata(text)
        self.assertNotIn("Add this setting", prose_only(text))
        self.assertNotIn("Timeouts", prose_only(text))
        self.assertIn("Add this setting", prose_only(repaired))
        self.assertIn("### Timeouts", prose_only(repaired))
        self.assertEqual(len(headings(repaired)), len(headings(text)) + 1)
        blocks = fenced_blocks(repaired)
        self.assertIn("```yml\nconfig:\n  follow_referrals: false\n```", blocks)
        self.assertIn("```yml\nconfig:\n  connect_timeout: 5000\n  response_timeout: 0\n```", blocks)
        # Every other code block is unchanged.
        swallowed = [b for b in fenced_blocks(text) if "follow_referrals: false" in b]
        self.assertEqual(len(swallowed), 1)
        self.assertEqual([b for b in fenced_blocks(text) if b not in swallowed],
                         [b for b in blocks if "follow_referrals: false" not in b and "connect_timeout" not in b])

    def test_key_value_backtick_repair_keeps_literals_and_exposes_prose(self):
        text = source(KEY_VALUE)
        repaired = apply_source_errata(text)
        self.assertNotIn("If this flag is enabled", prose_only(text))
        self.assertIn("If this flag is enabled", prose_only(repaired))
        inventory = protected_inventory(repaired)
        for literal in ("`{...}`", "`[...]`", "`<...>`", "`(...)`", '`"..."`', "`'...'`",
                        "`http://... (space)`", "`https:// (space)`", "`false`", "`true`",
                        '`{"key1=[a=b,c=d]&key2=value2"}`', '`{"key1": "[a=b,c=d]", "key2": "value2"}`'):
            self.assertIn(literal, inventory, literal)
        self.assertEqual(fenced_blocks(repaired), fenced_blocks(text))

    def test_replace_orphan_fence_gets_opening_fence(self):
        text = source(REPLACE)
        repaired = apply_source_errata(text)
        sentence = "The query returns the following results:"
        self.assertEqual(prose_only(text).count(sentence), text.count(sentence) - 1)
        self.assertEqual(prose_only(repaired).count(sentence), repaired.count(sentence))
        blocks = fenced_blocks(repaired)
        self.assertIn("```sql\n| where age > 30\n| fields state, age\n```", blocks)
        results = [b for b in blocks if "fetched rows / total rows = 3/3" in b]
        self.assertEqual(len(results), 1)
        self.assertTrue(results[0].startswith("```text\n"))
        self.assertIn(results[0], text)
        self.assertEqual(headings(repaired), headings(text))


class CompareTranslationErrataTests(unittest.TestCase):
    rules = TermRules.load(REPO / "translation/banned-terms.yml")

    def test_baseline_is_repaired_before_comparison(self):
        for page in (LDAP, KEY_VALUE, REPLACE):
            text = source(page)
            repaired = apply_source_errata(text)
            problems = compare_translation(text, add_modification_notice(repaired), self.rules)
            self.assertFalse([p for p in problems if "differ" in p], (page, problems))
            # A draft that keeps the malformed syntax no longer matches.
            stale = compare_translation(text, add_modification_notice(text), self.rules)
            self.assertTrue(any("differ" in p for p in stale), (page, stale))

    def test_current_text_is_never_repaired(self):
        # A current file byte-identical to the pinned baseline has the pinned
        # hash too; only the baseline side is repaired.
        text = source(LDAP)
        problems = compare_translation(text, text, self.rules)
        self.assertTrue(any("fenced code blocks differ" in p for p in problems), problems)


if __name__ == "__main__":
    unittest.main()
