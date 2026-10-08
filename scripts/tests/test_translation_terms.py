import unittest

from test_translation_helpers import REPO, config

from translation_pipeline.terms import TermRules, check_markdown, errors


class TermTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rules = TermRules.load(REPO / config.BANNED_TERMS_PATH)

    def hits(self, text):
        return [h.term for h in errors(check_markdown(text, self.rules))]

    def test_mainland_terms_in_prose_are_errors(self):
        self.assertEqual(self.hits("請安裝此軟件並設定默認值。"), ["軟件", "默認"])

    def test_protected_regions_are_ignored(self):
        text = ("使用 `軟件` 參數。\n\n```\n默認 = 1\n```\n"
                "[連結](/信息/) {% include 集群.html %} <!-- 搜索 -->\n")
        self.assertEqual(self.hits(text), [])

    def test_explicit_exceptions(self):
        self.assertEqual(self.hits("支持向量機與演算法在線上執行，用戶端與租用戶。"), [])
        self.assertEqual(self.hits("我們支持這個功能。"), ["支持"])

    def test_warnings_do_not_fail(self):
        hits = check_markdown("請設置用戶的配置。", self.rules)
        self.assertTrue(hits)
        self.assertEqual(errors(hits), [])

    def test_simplified_characters_are_errors(self):
        self.assertEqual(self.hits("这个設定"), ["这", "个"])
        self.assertEqual(self.hits("這個設定"), [])


if __name__ == "__main__":
    unittest.main()
