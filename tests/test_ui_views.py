from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from orchestrator.app_metadata import AppMetadata
from orchestrator.ui_views import is_markdown_filename


PROJECT_ROOT = Path(__file__).resolve().parents[1]


class AppMetadataTests(unittest.TestCase):
    def test_packaged_metadata_contains_repository_and_version(self) -> None:
        metadata = AppMetadata.load(PROJECT_ROOT / "app_metadata.json")
        self.assertEqual(metadata.name, "PMS-ORCHESTRATOR")
        self.assertEqual(metadata.version, "1.5")
        self.assertEqual(metadata.repository_url, "https://github.com/tz-dev/PMS-ORCHESTRATOR")
        self.assertEqual(metadata.license_file, "LICENSE")

    def test_license_file_is_read_verbatim(self) -> None:
        metadata = AppMetadata.load(PROJECT_ROOT / "app_metadata.json")
        content = metadata.read_license(PROJECT_ROOT)
        self.assertIn("LICENSE SCOPE NOTICE", content)
        self.assertIn("Apache License, Version 2.0", content)
        self.assertIn("Creative Commons Attribution-NonCommercial-ShareAlike 4.0", content)
        self.assertEqual(content, (PROJECT_ROOT / "LICENSE").read_text(encoding="utf-8").strip())

    def test_invalid_metadata_falls_back_safely(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "app_metadata.json"
            path.write_text("not-json", encoding="utf-8")
            metadata = AppMetadata.load(path)
            self.assertEqual(metadata.name, "PMS-ORCHESTRATOR")
            self.assertEqual(metadata.repository_url, "")


class MarkdownOutputTests(unittest.TestCase):
    def test_markdown_filename_detection(self) -> None:
        self.assertTrue(is_markdown_filename("article.md"))
        self.assertTrue(is_markdown_filename("ARTICLE.MARKDOWN"))
        self.assertFalse(is_markdown_filename("record.yaml"))
        self.assertFalse(is_markdown_filename("check.txt"))


if __name__ == "__main__":
    unittest.main()
