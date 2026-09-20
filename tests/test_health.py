from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from repoxray.gitinfo import inspect_git_repository
from repoxray.health import calculate_health
from repoxray.scanner import RepositoryScanner


class HealthTests(unittest.TestCase):
    def test_healthy_basics_earn_visible_points(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            (root / "README.md").write_text("# Demo", encoding="utf-8")
            (root / ".gitignore").write_text(".cache", encoding="utf-8")
            (root / "pyproject.toml").write_text("[project]", encoding="utf-8")
            (root / "tests").mkdir()
            (root / "tests" / "test_demo.py").write_text("pass", encoding="utf-8")
            (root / "src").mkdir()
            (root / "src" / "main.py").write_text("pass", encoding="utf-8")
            health = calculate_health(RepositoryScanner(root).scan(), inspect_git_repository(root), [], [])
            self.assertEqual(health.score, 85)
            self.assertIn("README found (+12)", health.positives)
            self.assertIn("Not a Git repository", health.warnings)
            self.assertTrue(health.rules)
