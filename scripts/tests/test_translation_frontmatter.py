import copy
import unittest

import yaml

from test_translation_helpers import INDEX_PAGE, LANDING_PAGE, MATCH_PAGE, NOTICE

from translation_pipeline.frontmatter import (FrontMatterError, add_modification_notice,
                                              has_modification_notice, original_front_matter, rewrite,
                                              split_document, structural_problems, translatable_fields)
from translation_pipeline.protect import Protector, tokens_in

LANDING_IDS = {
    "fm.title",
    "fm.more_cards.0.heading", "fm.more_cards.0.description",
    "fm.more_cards.1.heading", "fm.more_cards.1.description",
    "fm.features.0.heading", "fm.features.0.description", "fm.features.0.image_alt",
    "fm.flows.0.heading", "fm.flows.0.list.0", "fm.flows.0.list.1",
}


def zh_all(data):
    return {sid: f"譯{n}" for n, sid in enumerate(sorted(translatable_fields(data)))}


class FrontMatterTests(unittest.TestCase):
    def test_only_visible_fields_are_translatable(self):
        doc = split_document(INDEX_PAGE)
        self.assertEqual(set(translatable_fields(doc.data)), {
            "fm.title", "fm.description", "fm.next_steps.0.heading", "fm.next_steps.0.description"})
        doc = split_document(MATCH_PAGE)
        self.assertEqual(set(translatable_fields(doc.data)), {"fm.title"})

    def test_original_front_matter_keeps_ancestry(self):
        doc = split_document(MATCH_PAGE)
        self.assertEqual(original_front_matter(doc.data), {
            "title": "Match query", "parent": "Full-text queries", "grand_parent": "Query DSL"})

    def test_rewrite_translates_fields_and_keeps_structure(self):
        doc = split_document(INDEX_PAGE)
        translations = {
            "fm.title": "入門: \"指南\" #1",          # YAML-special characters
            "fm.description": "開始使用 OpenSearch。",
            "fm.next_steps.0.heading": "OpenSearch 簡介",
            "fm.next_steps.0.description": "了解 OpenSearch 如何儲存資料。",
        }
        head = rewrite(doc, translations)
        data = yaml.safe_load(head.split("---\n")[1])
        self.assertEqual(data["title"], translations["fm.title"])
        self.assertEqual(data["next_steps"][0]["link"], "/getting-started/intro/")
        self.assertEqual(data["permalink"], "/getting-started/")
        self.assertEqual(data["nav_order"], 1)
        self.assertEqual(structural_problems(doc.data, data), [])
        self.assertIn("nav_order: 1\nhas_children: true\npermalink: /getting-started/\n", head)

    def test_rewrite_handles_multiline_values_and_keeps_parent(self):
        text = ("---\ntitle: >\n  A folded\n  title\nparent: Parent page\nnav_order: 2\n---\nBody\n")
        doc = split_document(text)
        head = rewrite(doc, {"fm.title": "摺疊標題"})
        data = yaml.safe_load(head.split("---\n")[1])
        self.assertEqual(data, {"title": "摺疊標題", "parent": "Parent page", "nav_order": 2})

    def test_rewrite_rejects_non_translatable_field(self):
        doc = split_document(MATCH_PAGE)
        with self.assertRaises(FrontMatterError):
            rewrite(doc, {"fm.parent": "全文查詢"})

    def test_structural_problems_detect_translated_parent_and_links(self):
        base = split_document(INDEX_PAGE).data
        changed = yaml.safe_load(yaml.safe_dump(base))
        changed["title"] = "入門"
        self.assertEqual(structural_problems(base, changed), [])
        changed["permalink"] = "/zh/"
        changed["next_steps"][0]["link"] = "/other/"
        problems = structural_problems(base, changed)
        self.assertTrue(any("permalink" in p for p in problems))
        self.assertTrue(any("next_steps" in p for p in problems))
        match = split_document(MATCH_PAGE).data
        translated_parent = dict(match, parent="全文查詢")
        self.assertTrue(any("parent" in p for p in structural_problems(match, translated_parent)))

    def test_empty_translated_title_is_a_problem(self):
        base = split_document(MATCH_PAGE).data
        self.assertTrue(structural_problems(base, dict(base, title="")))


    # -- nested card lists ---------------------------------------------------------------
    def test_nested_visible_fields_have_stable_path_ids(self):
        doc = split_document(LANDING_PAGE)
        fields = translatable_fields(doc.data)
        self.assertEqual(set(fields), LANDING_IDS)
        self.assertEqual(fields["fm.flows.0.list.0"], "<b>Platform:</b> OpenSearch")
        for kept in ("link", "image", "redirect_from", "seo", "layout"):
            self.assertFalse(any(sid.endswith("." + kept) or sid.startswith(f"fm.{kept}") for sid in fields), kept)

    def test_keys_that_cannot_form_ids_and_structural_roots_are_skipped(self):
        data = {"title": "T", "cards.v2": [{"heading": "H"}], "seo": {"title": "S"},
                "parent": "P", "items": [{"link": "/x/", "id": "a", "icon": "i", "a.b": {"heading": "Z"}}],
                "tags": ["plain list items are not visible text"], "next_steps": [{"heading": " "}]}
        self.assertEqual(set(translatable_fields(data)), {"fm.title"})

    def test_rewrite_nested_roots_keeps_comments_and_unrelated_lines(self):
        doc = split_document(LANDING_PAGE)
        translations = zh_all(doc.data)
        head = rewrite(doc, translations)
        raw = head.split("---\n")[1]
        data = yaml.safe_load(raw)
        self.assertEqual(translatable_fields(data), translations)
        self.assertEqual(structural_problems(doc.data, data), [])
        for line in ("layout: default", "has_children: true", "nav_order: 5",
                     "# Cards rendered by the landing layout.", "redirect_from:", "  - /tutorials/old/",
                     "seo:", "  type: TechArticle"):
            self.assertIn(line + "\n", raw)
        self.assertEqual([c["link"] for c in data["more_cards"]], ["/vector-search/", "/getting-started/"])
        self.assertEqual(data["features"][0]["image_alt"], translations["fm.features.0.image_alt"])
        # Only the changed root is re-dumped.
        only_flows = rewrite(doc, {"fm.flows.0.list.1": "<b>模型：</b> Anthropic Claude"})
        self.assertIn('  - heading: "Vector search"\n', only_flows)
        self.assertIn("<b>模型：</b> Anthropic Claude", only_flows)

    def test_rewrite_rejects_non_visible_nested_paths(self):
        doc = split_document(LANDING_PAGE)
        for sid in ("fm.more_cards.0.link", "fm.redirect_from.0", "fm.more_cards.5.heading"):
            with self.assertRaises(FrontMatterError, msg=sid):
                rewrite(doc, {sid: "譯"})

    def test_nested_structure_changes_are_rejected(self):
        base = split_document(LANDING_PAGE).data
        good = yaml.safe_load(split_document(rewrite(split_document(LANDING_PAGE), zh_all(base)) + "x").raw)
        self.assertEqual(structural_problems(base, good), [])

        def changed(mutate):
            data = copy.deepcopy(good)
            mutate(data)
            return structural_problems(base, data)
        cases = {
            "nested link": lambda d: d["more_cards"][0].update(link="/zh/vector-search/"),
            "card order": lambda d: d["more_cards"].reverse(),
            "card count": lambda d: d["more_cards"].pop(),
            "list count": lambda d: d["flows"][0]["list"].append("額外"),
            "image": lambda d: d["features"][0].update(image="/x.png"),
            "added key": lambda d: d["features"][0].update(text="新增"),
            "redirect": lambda d: d["redirect_from"].append("/zh/"),
        }
        for label, mutate in cases.items():
            self.assertTrue(any("differs" in p for p in changed(mutate)), label)
        for label, mutate in {"empty": lambda d: d["more_cards"][1].update(description=""),
                              "missing": lambda d: d["flows"][0]["list"].__setitem__(0, None),
                              "removed": lambda d: d["features"][0].pop("heading")}.items():
            self.assertTrue(any("missing or empty" in p for p in changed(mutate)), label)

    def test_markup_inside_front_matter_strings_is_protected(self):
        fields = translatable_fields(split_document(LANDING_PAGE).data)
        p = Protector()
        protected = p.protect_inline(fields["fm.more_cards.0.description"])
        self.assertEqual(sorted(p.restore(t) for t in tokens_in(protected)),
                         sorted(["<b>", "</b>", "`knn`", "{{site.url}}{{site.baseurl}}/vector-search/"]))
        protected = p.protect_inline(fields["fm.flows.0.list.0"])
        self.assertEqual(p.restore(protected), "<b>Platform:</b> OpenSearch")
        self.assertEqual(len(tokens_in(protected)), 2)

    # -- modification notice --------------------------------------------------------------
    def test_modification_notice_is_a_comment_after_the_opening_delimiter(self):
        once = add_modification_notice(MATCH_PAGE)
        self.assertTrue(once.startswith("---\n" + NOTICE + "\nlayout: default\n"))
        self.assertEqual(add_modification_notice(once), once, "idempotent")
        doc = split_document(once)
        self.assertTrue(has_modification_notice(doc))
        self.assertEqual(doc.data, split_document(MATCH_PAGE).data, "no YAML data key added")
        self.assertEqual(doc.body, split_document(MATCH_PAGE).body, "body untouched")
        self.assertFalse(has_modification_notice(split_document(MATCH_PAGE)))
        crlf = add_modification_notice("---\r\ntitle: A\r\n---\r\nBody\r\n")
        self.assertEqual(crlf, "---\r\n" + NOTICE + "\r\ntitle: A\r\n---\r\nBody\r\n")
        with self.assertRaises(FrontMatterError):
            add_modification_notice("# No front matter\n")


if __name__ == "__main__":
    unittest.main()
