import unittest

from test_translation_helpers import MATCH_PAGE, REPO, config

from translation_pipeline.protect import (Protector, fenced_blocks, normalize_block_tokens,
                                          placeholder_problems, prose_only, protected_inventory, tokens_in)


class ProtectTests(unittest.TestCase):
    def protect(self, text):
        p = Protector()
        return p, p.protect_body(text)

    def test_round_trip_is_lossless(self):
        p, protected = self.protect(MATCH_PAGE)
        self.assertEqual(p.restore(protected), MATCH_PAGE)

    def test_fenced_code_is_one_block_token_byte_for_byte(self):
        text = "Intro\n\n1. Step\n\n   ```bash\n   curl -X GET \"localhost:9200\"\n   ```\n\nAfter\n"
        p, protected = self.protect(text)
        self.assertNotIn("curl", protected)
        token = next(iter(p.block_tokens))
        self.assertEqual(p.store[token], "   ```bash\n   curl -X GET \"localhost:9200\"\n   ```")
        self.assertEqual(fenced_blocks(text), [p.store[token]])

    def test_longer_fence_contains_shorter_fence_and_tilde_fence(self):
        text = "````md\n```json\n{}\n```\n````\n\n~~~\nraw ~~~ text\n~~~\n"
        p, protected = self.protect(text)
        self.assertEqual(len(p.block_tokens), 2)
        self.assertEqual(protected.count("⟦P"), 2)
        self.assertEqual(p.restore(protected), text)

    def test_unclosed_fence_runs_to_end(self):
        text = "Para\n\n```\ncode without close\n"
        p, protected = self.protect(text)
        self.assertEqual(p.restore(protected), text)
        self.assertNotIn("code without", protected)

    def test_liquid_capture_raw_comment_and_tags_are_protected(self):
        text = ("{% capture step1 %}\nPUT /index\n{% endcapture %}\n\n"
                "{% raw %}{{ not liquid }}{% endraw %} text {{ site.url }} and {%- comment -%}x{%- endcomment -%}\n"
                "{% include copy.html id=\"a\" %}\n")
        p, protected = self.protect(text)
        for fragment in ("PUT /index", "capture", "not liquid", "site.url", "comment", "include"):
            self.assertNotIn(fragment, protected)
        self.assertIn(" text ", protected)
        self.assertEqual(p.restore(protected), text)

    def test_capture_with_nested_fence_restores(self):
        text = "{% capture c %}\n```json\n{\"a\": 1}\n```\n{% endcapture %}\n"
        p, protected = self.protect(text)
        self.assertEqual(len(tokens_in(protected)), 1)
        self.assertEqual(p.restore(protected), text)

    def test_link_destinations_ref_labels_and_urls(self):
        text = ("See [the docs]({{site.url}}{{site.baseurl}}/api/#path \"Title\") and ![img](/a.png).\n"
                "Use [ref link][my-ref] or <https://example.com>. Visit https://opensearch.org/x.\n\n"
                "[my-ref]: https://example.com/ref\n")
        p, protected = self.protect(text)
        for fragment in ("site.url", "/a.png", "my-ref", "example.com", "opensearch.org"):
            self.assertNotIn(fragment, protected)
        self.assertIn("[the docs](", protected)
        self.assertIn("Visit ⟦", protected)
        self.assertRegex(protected, r"Visit ⟦P\d+⟧\.\n", "trailing period stays outside the URL token")
        self.assertEqual(p.restore(protected), text)

    def test_html_comments_tags_ial_and_footnotes(self):
        text = "<!-- vale off -->\nText<br>more <b>bold</b>[^1]\n{: .note}\n## Head {#custom-id}\n<!-- vale on -->\n"
        p, protected = self.protect(text)
        for fragment in ("vale", "<br>", "<b>", ".note", "custom-id", "[^1]"):
            self.assertNotIn(fragment, protected)
        self.assertIn("## Head", protected)
        self.assertEqual(p.restore(protected), text)

    def test_url_boundary_unchanged_next_to_cjk(self):
        self.assertEqual(protected_inventory("Visit https://opensearch.org/docs."),
                         protected_inventory("請造訪https://opensearch.org/docs。"))

    def test_placeholder_integrity_problems(self):
        p, protected = self.protect("Text `a` and `b`.\n\n```\ncode\n```\n")
        tokens = sorted(tokens_in(protected), key=lambda t: int(t[2:-1]))
        block = next(iter(p.block_tokens))
        self.assertEqual(placeholder_problems(protected, protected, p.block_tokens), [])
        dropped = protected.replace(tokens[0], "", 1)
        self.assertTrue(any("missing" in x for x in placeholder_problems(protected, dropped, p.block_tokens)))
        doubled = protected + tokens[0]
        self.assertTrue(any("unexpected" in x for x in placeholder_problems(protected, doubled, p.block_tokens)))
        inline_block = protected.replace("\n" + block, " " + block)
        self.assertTrue(any("own line" in x for x in placeholder_problems(protected, inline_block, p.block_tokens)))
        self.assertTrue(placeholder_problems(protected, protected + " ⟦P99", p.block_tokens))

    def test_indented_block_placeholder_is_normalized(self):
        p, protected = self.protect("Para\n\n```\nx\n```\n")
        block = next(iter(p.block_tokens))
        indented = protected.replace(block, "   " + block)
        self.assertEqual(normalize_block_tokens(indented, p.block_tokens), protected)

    def test_unknown_token_is_rejected(self):
        with self.assertRaises(ValueError):
            Protector().restore("⟦P5⟧")

    def test_copyright_license_attribution_link_paragraph_is_verbatim(self):
        notice = 'Tiles are generated per [Terms of Use](https://example.org/terms/) and [Copyright and License for OpenStreetMap](https://www.openstreetmap.org/copyright).'
        protector = Protector()
        protected = protector.protect_body(notice)
        self.assertNotIn('Tiles are generated', protected)
        self.assertEqual(protector.restore(protected), notice)

    def test_prose_only_drops_code_and_urls(self):
        prose = prose_only("中文 `軟件` 內容\n\n```\n軟件\n```\n[連結](/軟件/) {{ 軟件 }}")
        self.assertNotIn("軟件", prose)
        self.assertIn("中文", prose)

    def test_pilot_pages_round_trip(self):
        for page in config.PILOT_PATHS:
            path = REPO / config.SOURCE_STORE_DIR / page
            if not path.exists():
                continue
            text = path.read_text(encoding="utf-8")
            p, protected = self.protect(text)
            self.assertEqual(p.restore(protected), text, page)


    def test_legal_notices_are_protected_verbatim(self):
        text = ("Intro paragraph.\n\nCopyright 2024 OpenSearch Contributors\n"
                "SPDX-License-Identifier: Apache-2.0\n\n"
                "See [Copyright and License for OpenStreetMap](https://www.openstreetmap.org/copyright).\n")
        p, protected = self.protect(text)
        self.assertEqual(p.restore(protected), text)
        self.assertNotIn("Copyright 2024", protected)
        self.assertNotIn("SPDX", protected)
        self.assertIn("See [Copyright and License for OpenStreetMap]", protected,
                      "link text naming a license page is ordinary prose")
        self.assertIn("Copyright 2024 OpenSearch Contributors", protected_inventory(text))
        changed = text.replace("Copyright 2024 OpenSearch Contributors", "著作權 2024 OpenSearch 貢獻者")
        self.assertNotEqual(protected_inventory(changed), protected_inventory(text))
        legal_tokens = [t for t in tokens_in(protected) if p.store[t].startswith(("Copyright", "SPDX"))]
        self.assertTrue(legal_tokens and all(t in p.block_tokens for t in legal_tokens))


if __name__ == "__main__":
    unittest.main()
