from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from repoxray.analyzer import detect_languages
from repoxray.scanner import RepositoryScanner


class LanguageDetectionTests(unittest.TestCase):
    def test_detects_languages_and_percentages_from_file_size(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            (root / "app.py").write_text("x" * 30, encoding="utf-8")
            (root / "site.js").write_text("x" * 10, encoding="utf-8")
            languages = detect_languages(RepositoryScanner(root).scan())
            self.assertEqual(languages["Python"]["files"], 1)
            self.assertEqual(languages["Python"]["percentage"], 75.0)
            self.assertEqual(languages["JavaScript"]["percentage"], 25.0)
