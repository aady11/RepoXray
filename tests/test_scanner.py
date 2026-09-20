from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from repoxray.scanner import RepositoryScanner, extension_breakdown, format_size


class RepositoryScannerTests(unittest.TestCase):
    def test_scans_files_calculates_size_and_skips_standard_directories(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            (root / "src").mkdir()
            (root / "src" / "main.py").write_text("print('x')\n", encoding="utf-8")
            (root / ".hidden").write_text("hidden", encoding="utf-8")
            (root / "node_modules").mkdir()
            (root / "node_modules" / "package.js").write_text("ignored", encoding="utf-8")
            scan = RepositoryScanner(root).scan()
            self.assertEqual(scan.file_count, 2)
            self.assertEqual(
                scan.size_bytes,
                (root / "src" / "main.py").stat().st_size + (root / ".hidden").stat().st_size,
            )
            self.assertEqual(scan.hidden_file_count, 1)
            self.assertIn("node_modules", scan.ignored_paths)
            self.assertEqual(extension_breakdown(scan), {".py": 1, "[no extension]": 1})

    def test_formats_human_readable_sizes(self) -> None:
        self.assertEqual(format_size(512), "512 B")
        self.assertEqual(format_size(1536), "1.5 KB")
