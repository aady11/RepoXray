from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from repoxray.scanner import RepositoryScanner
from repoxray.secrets import scan_for_secrets


class SecretScannerTests(unittest.TestCase):
    def test_detects_fake_key_without_exposing_its_value(self) -> None:
        fake_value = "not_a_real_token_123456789"
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            (root / "settings.py").write_text("API_KEY = '{0}'\n".format(fake_value), encoding="utf-8")
            findings = scan_for_secrets(RepositoryScanner(root).scan().files)
            self.assertEqual(len(findings), 1)
            self.assertEqual(findings[0].severity, "HIGH")
            self.assertEqual(findings[0].line, 1)
            self.assertNotIn(fake_value, str(findings[0].to_dict()))

    def test_ignores_obvious_placeholder_values(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            (root / "example.py").write_text("API_KEY = 'placeholder'\n", encoding="utf-8")
            self.assertEqual(scan_for_secrets(RepositoryScanner(root).scan().files), [])
