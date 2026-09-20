"""A deliberately transparent, non-scientific repository health score."""

from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Sequence

from .models import GitInfo, HealthReport, LargeFile, ScanResult, SecretFinding


HEALTH_RULES: Sequence[Dict[str, object]] = (
    {"id": "base", "points": 35, "description": "Every repository starts at 35 points."},
    {"id": "readme", "points": 12, "description": "README present at the repository root."},
    {"id": "gitignore", "points": 10, "description": ".gitignore present at the repository root."},
    {"id": "tests", "points": 10, "description": "A tests, test, or spec directory is present."},
    {"id": "metadata", "points": 8, "description": "Recognized package metadata is present."},
    {"id": "structure", "points": 5, "description": "A conventional source directory is present."},
    {"id": "git", "points": 5, "description": "Target is a local Git repository."},
    {"id": "no_secrets", "points": 5, "description": "No heuristic secret findings."},
    {"id": "large_file", "points": -8, "cap": -16, "description": "Each large file, capped at two."},
    {"id": "secret_high", "points": -20, "description": "Each high-confidence secret finding."},
    {"id": "secret_medium", "points": -8, "description": "Each medium-confidence secret finding."},
    {"id": "generated_junk", "points": -5, "description": "Three or more top-level ignored generated directories."},
)
METADATA_FILES = {"pyproject.toml", "package.json", "setup.py", "setup.cfg", "cargo.toml", "go.mod", "pom.xml"}
SOURCE_DIRECTORIES = {"src", "app", "lib", "repoxray", "packages"}
TEST_DIRECTORIES = {"tests", "test", "spec", "specs"}
GENERATED_DIRECTORIES = {"node_modules", "dist", "build", ".venv", "venv", "__pycache__"}


def calculate_health(
    scan: ScanResult, git: GitInfo, secrets: Sequence[SecretFinding], large_files: Sequence[LargeFile]
) -> HealthReport:
    """Score a repository from the public ``HEALTH_RULES`` table."""
    root_names = {file.relative_path.lower() for file in scan.files if "/" not in file.relative_path}
    directory_names = _directory_names(scan)
    score = 35
    positives: List[str] = []
    warnings: List[str] = []

    def reward(condition: bool, points: int, positive: str, warning: str) -> None:
        nonlocal score
        if condition:
            score += points
            positives.append(positive)
        else:
            warnings.append(warning)

    reward("readme.md" in root_names or "readme" in root_names, 12, "README found (+12)", "No README found")
    reward(".gitignore" in root_names, 10, ".gitignore found (+10)", "No .gitignore found")
    reward(bool(directory_names & TEST_DIRECTORIES), 10, "Tests directory found (+10)", "No tests directory found")
    reward(bool(root_names & METADATA_FILES), 8, "Package metadata found (+8)", "No recognized package metadata found")
    reward(bool(directory_names & SOURCE_DIRECTORIES), 5, "Conventional source directory found (+5)", "No conventional source directory found")
    if git.is_repository:
        score += 5
        positives.append("Local Git repository detected (+5)")
    else:
        warnings.append("Not a Git repository")
    if not secrets:
        score += 5
        positives.append("No obvious secrets found (+5)")
    else:
        high_count = sum(finding.severity == "HIGH" for finding in secrets)
        medium_count = sum(finding.severity == "MEDIUM" for finding in secrets)
        low_count = sum(finding.severity == "LOW" for finding in secrets)
        score -= high_count * 20 + medium_count * 8 + low_count * 3
        warnings.append("{0} possible sensitive item(s) found".format(len(secrets)))
    if large_files:
        penalty = min(len(large_files), 2) * 8
        score -= penalty
        warnings.append("{0} large file(s) detected (-{1})".format(len(large_files), penalty))
    generated_count = sum(
        "/" not in path and Path(path).name in GENERATED_DIRECTORIES
        for path in scan.ignored_paths
    )
    if generated_count >= 3:
        score -= 5
        warnings.append("Several generated directories were ignored (-5)")
    return HealthReport(max(0, min(100, score)), positives, warnings, [dict(rule) for rule in HEALTH_RULES])


def _directory_names(scan: ScanResult) -> set[str]:
    directories = set()
    for file in scan.files:
        parent = Path(file.relative_path).parent
        if str(parent) != ".":
            directories.update(part.lower() for part in parent.parts)
    return directories
