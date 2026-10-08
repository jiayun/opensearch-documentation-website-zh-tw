import unittest

from test_translation_helpers import config

from translation_pipeline.protect import Protector, tokens_in
from translation_pipeline.segment import heading_levels, split_body


def paragraph(n: int, words: int = 60) -> str:
    return " ".join(f"word{n}" for _ in range(words)) + "\n\n"


class SegmentTests(unittest.TestCase):
    def test_small_body_is_one_chunk(self):
        chunks = split_body("\n# Title\n\nText.\n", config.CHUNK_LIMIT)
        self.assertEqual(len(chunks), 1)
        self.assertEqual(chunks[0].lead, "\n")
        self.assertEqual(chunks[0].core, "# Title\n\nText.")
        self.assertEqual(chunks[0].trail, "\n")

    def test_large_body_splits_on_paragraphs_and_rejoins_exactly(self):
        body = "".join(f"## Section {i}\n\n" + paragraph(i) * 5 for i in range(20))
        self.assertGreater(len(body), 12000)
        chunks = split_body(body, 12000)
        self.assertGreater(len(chunks), 1)
        self.assertEqual("".join(c.text for c in chunks), body)
        for chunk in chunks:
            self.assertLessEqual(len(chunk.text), 12000)
            self.assertTrue(chunk.core.startswith("## Section"), "prefers heading boundaries")

    def test_code_placeholders_are_never_split_and_size_uses_original_text(self):
        p = Protector()
        code = "```json\n" + "{\"k\": 1}\n" * 1500 + "```\n"
        body = p.protect_body("Intro.\n\n" + code + "\nAfter " + paragraph(1) + "## Next\n\nMore.\n")
        chunks = split_body(body, 12000, size=lambda s: len(p.restore(s)))
        self.assertGreater(len(chunks), 1)
        joined = "".join(c.text for c in chunks)
        self.assertEqual(p.restore(joined), p.restore(body))
        self.assertEqual(sum(len(tokens_in(c.core)) for c in chunks), len(tokens_in(body)))

    def test_single_oversized_block_falls_back_to_lines(self):
        table = "| a | b |\n|---|---|\n" + "".join(f"| row {i} | {'x' * 80} |\n" for i in range(300))
        chunks = split_body(table, 12000)
        self.assertGreater(len(chunks), 1)
        self.assertEqual("".join(c.text for c in chunks), table)
        self.assertTrue(all(c.core.startswith("|") for c in chunks))

    def test_heading_levels(self):
        self.assertEqual(heading_levels("# A\ntext\n## B\n#nohead\n### C"), [1, 2, 3])


if __name__ == "__main__":
    unittest.main()
