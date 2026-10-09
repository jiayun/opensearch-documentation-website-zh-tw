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

    def test_get_settings_response_captures_expose_prose_only(self):
        text = (REPO / config.SOURCE_STORE_DIR / "_api-reference/index-apis/get-settings.md").read_text(encoding="utf-8")
        p, protected = self.protect(text)
        self.assertEqual(p.restore(protected), text)
        for prose in ("## Example response \n", "By default, settings are returned in nested format:",
                      "## Example response: Flat format", "settings are returned in flattened format:"):
            self.assertIn(prose, protected)
        for fragment in ("GET /books/_settings", "client.indices.get_settings", "number_of_shards",
                         "capture", "default_response", "flat_settings=true", "{{", "{%"):
            self.assertNotIn(fragment, protected)
        # Captures rendered by code-block.html stay one block each.
        originals = set(p.protected_originals(protected))
        self.assertIn("{% capture step1_rest %}\nGET /books/_settings\n{% endcapture %}", originals)
        self.assertTrue(any(o.startswith("{% capture step1_python %}") and o.endswith("{% endcapture %}")
                            for o in originals))
        tags = [t for t in tokens_in(protected)
                if p.store[t] in ("{% capture default_response %}", "{% capture flat_response %}", "{% endcapture %}")]
        self.assertEqual(len(tags), 4)
        self.assertTrue(all(t in p.block_tokens for t in tags))
        moved = protected.replace(tags[-1], "說明 " + tags[-1])
        self.assertTrue(any("own line" in x for x in placeholder_problems(protected, moved, p.block_tokens)))

        translated = (text.replace("## Example response \n", "## 範例回應\n")
                      .replace("By default, settings are returned in nested format:", "預設情況下，設定會以巢狀格式傳回：")
                      .replace("## Example response: Flat format", "## 範例回應：扁平格式")
                      .replace("When you specify `flat_settings=true`, settings are returned in flattened format:",
                               "指定 `flat_settings=true` 時，設定會以扁平格式傳回："))
        self.assertEqual(translated.count("By default"), 0)
        self.assertEqual(protected_inventory(translated), protected_inventory(text))
        changed_json = translated.replace('"number_of_shards": "2"', '"number_of_shards": "3"', 1)
        self.assertNotEqual(protected_inventory(changed_json), protected_inventory(text))
        changed_rest = translated.replace("{% capture step1_rest %}\nGET /books/_settings",
                                          "{% capture step1_rest %}\nGET /books/_mapping")
        self.assertNotEqual(protected_inventory(changed_rest), protected_inventory(text))
        changed_tag = translated.replace("{{ flat_response }}", "{{ flat_responses }}")
        self.assertNotEqual(protected_inventory(changed_tag), protected_inventory(text))

    def test_code_captures_and_comments_stay_whole(self):
        cases = {
            "{% capture step1_rest %}\n## Heading\n\nThis is a sentence of prose.\n{% endcapture %}\n"
            "{% include code-block.html\n    rest=step1_rest %}\n": "This is a sentence",
            "{% capture req %}\nGET /_cat/indices?v\n{% endcapture %}\n{{ req }}\n": "GET",
            "{% capture snippet %}\nresponse = client.search(index = \"books\")\nprint(response)\n"
            "{% endcapture %}\n{{ snippet }}\n": "client.search",
            "{% comment %}\n## Hidden\n\nThis note is for maintainers only.\n{% endcomment %}\n": "maintainers",
        }
        for text, hidden in cases.items():
            p, protected = self.protect(text)
            self.assertNotIn(hidden, protected, text)
            self.assertEqual(p.restore(protected), text)

    def test_prose_capture_without_heading_is_translatable(self):
        text = "{% capture note %}\nThis setting applies to all indexes.\n{% endcapture %}\n{{ note }}\n"
        p, protected = self.protect(text)
        self.assertIn("This setting applies to all indexes.", protected)
        self.assertEqual(p.restore(protected), text)
        translated = text.replace("This setting applies to all indexes.", "此設定適用於所有索引。")
        self.assertEqual(protected_inventory(translated), protected_inventory(text))

    def test_raw_with_code_literals_exposes_only_conjunction(self):
        text = (REPO / config.SOURCE_STORE_DIR / "_ingest-pipelines/accessing-data.md").read_text(encoding="utf-8")
        line = ("Use triple curly braces ({% raw %}`{{{` and `}}}`{% endraw %}) for unescaped field values.")
        self.assertIn(line, text)
        p, protected = self.protect(text)
        self.assertEqual(p.restore(protected), text)
        self.assertRegex(protected, r"Use triple curly braces \(⟦P\d+⟧ and ⟦P\d+⟧\) for unescaped field values\.")
        self.assertNotIn("{{{", protected)
        self.assertNotIn("}}}", protected)
        originals = p.protected_originals(protected)
        self.assertIn("{% raw %}`{{{`", originals)
        self.assertIn("`}}}`{% endraw %}", originals)

        translated = text.replace(line, "使用三層大括號（{% raw %}`{{{` 與 `}}}`{% endraw %}）插入未逸出的欄位值。")
        self.assertEqual(protected_inventory(translated), protected_inventory(text))
        moved = text.replace(line, "使用三層大括號（{% raw %}`{{{` 與{% endraw %} `}}}`）插入未逸出的欄位值。")
        self.assertNotEqual(protected_inventory(moved), protected_inventory(text))
        changed = text.replace(line, "使用三層大括號（{% raw %}`{{{` 與 `}}`{% endraw %}）插入未逸出的欄位值。")
        self.assertNotEqual(protected_inventory(changed), protected_inventory(text))

    def test_raw_with_liquid_syntax_stays_whole(self):
        for raw in ("{% raw %}`{{leader_index}}`{% endraw %}",
                    "{% raw %}{{a}} and {{b}}{% endraw %}",
                    "{% raw %}`{{a}}` and {{b}} or `{{c}}`{% endraw %}",
                    "{% raw %}`{{a}}` / `{{b}}`{% endraw %}"):
            text = f"Use {raw} here.\n"
            p, protected = self.protect(text)
            self.assertRegex(protected, r"^Use ⟦P\d+⟧ here\.\n$", raw)
            self.assertIn(raw, p.protected_originals(protected))

    def test_liquid_block_pages_round_trip(self):
        for path in sorted((REPO / config.SOURCE_STORE_DIR).rglob("*.md")):
            text = path.read_text(encoding="utf-8")
            if "{% raw" not in text and "{% capture" not in text:
                continue
            p, protected = self.protect(text)
            self.assertEqual(p.restore(protected), text, path)

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
