import unittest
from test_translation_helpers import REPO
from translation_pipeline.prompts import normalize_taiwan_prose
from translation_pipeline.protect import Protector


class TaiwanNormalizationTests(unittest.TestCase):
    def test_it_vocabulary_is_corrected_without_changing_protected_code(self):
        original = '添加設定、取消註釋及本地儲存的檢視。\n\n```json\n{"name":"本地儲存","note":"註釋"}\n```\n'
        protector = Protector()
        protected = protector.protect_body(original)
        corrected = protector.restore(normalize_taiwan_prose(protected))
        self.assertIn('新增設定、取消註解及本機儲存', corrected)
        self.assertIn('{"name":"本地儲存","note":"註釋"}', corrected)

    def test_non_it_word_exception_is_preserved(self):
        self.assertEqual(normalize_taiwan_prose('添加劑與本地化'), '添加劑與本地化')

    def test_view_chart_is_not_corrupted_by_noun_view_replacement(self):
        value = '檢視圖表並檢視圖層，接著建立視圖。'
        expected = '檢視圖表並檢視圖層，接著建立檢視。'
        self.assertEqual(normalize_taiwan_prose(value), expected)
        self.assertEqual(normalize_taiwan_prose(expected), expected)

    def test_product_codes_use_product_identifiers_without_touching_code(self):
        protector = Protector()
        source = '產品代碼\n\n```json\n{"title":"產品代碼"}\n```\n'
        corrected = protector.restore(normalize_taiwan_prose(protector.protect_body(source)))
        self.assertTrue(corrected.startswith('產品代號'))
        self.assertIn('{"title":"產品代碼"}', corrected)


if __name__ == '__main__': unittest.main()
