"""Meaningful regression tests for preserved licenses and file notices."""
import importlib.util
from pathlib import Path
import tempfile
import unittest

MODULE_PATH = Path(__file__).resolve().parents[1] / "license_check.py"
SPEC = importlib.util.spec_from_file_location("license_check", MODULE_PATH)
license_check = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(license_check)


class LicenseTests(unittest.TestCase):
    def test_front_matter_notice_stays_a_yaml_comment(self):
        source = "---\ntitle: Example\nparent: API\n---\n# Example\n"
        result = license_check.modification_notice(source, ".md")
        self.assertTrue(result.startswith("---\n# Modified by"))
        self.assertIn("title: Example\nparent: API\n---\n# Example\n", result)
        self.assertEqual(result, license_check.modification_notice(result, ".md"))

    def test_shebang_survives(self):
        result = license_check.modification_notice("#!/bin/bash\nset -e\n", ".sh")
        self.assertTrue(result.startswith("#!/bin/bash\n# Modified by"))

    def test_json_remains_parseable(self):
        import json
        result = json.loads(license_check.modification_notice('{"current":"3.9"}', ".json"))
        self.assertEqual("3.9", result["current"])
        self.assertEqual(license_check.MARKER, result["_translation_notice"])

    def test_removing_copyright_or_spdx_is_detected(self):
        original = "# Copyright OpenSearch Contributors\n# SPDX-License-Identifier: BSD-3-Clause\ncode\n"
        self.assertEqual([], license_check.retained_notices(original, original + "change\n"))
        self.assertEqual(2, len(license_check.retained_notices(original, "code\n")))

    def test_removing_embedded_permission_is_detected(self):
        before = "{% comment %}\nCopyright Author\nPermission is hereby granted to copy.\nTHE SOFTWARE IS PROVIDED AS IS.\n{% endcomment %}"
        after = "{% comment %}\nCopyright Author\n{% endcomment %}"
        self.assertIn("embedded permission and disclaimer text", license_check.retained_notices(before, after))

    def test_missing_built_notices_fail(self):
        with tempfile.TemporaryDirectory() as folder:
            errors = license_check.check_site(Path(folder))
        self.assertTrue(any("built license missing" in e for e in errors))
        self.assertIn("built attribution page missing", errors)


if __name__ == "__main__":
    unittest.main()
