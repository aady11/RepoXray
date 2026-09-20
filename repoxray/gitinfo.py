"""Safe local Git metadata collection."""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Optional

from .models import GitInfo


def inspect_git_repository(path: Path) -> GitInfo:
    """Read basic Git state without changing the target repository."""
    inside = _git(path, "rev-parse", "--is-inside-work-tree")
    if inside is None or inside.strip().lower() != "true":
        return GitInfo(is_repository=False)
    branch = _git(path, "branch", "--show-current") or None
    status = _git(path, "status", "--porcelain")
    commit_count_raw = _git(path, "rev-list", "--count", "HEAD")
    remote_url = _git(path, "config", "--get", "remote.origin.url") or None
    try:
        commit_count = int(commit_count_raw) if commit_count_raw else 0
    except ValueError:
        commit_count = None
    return GitInfo(
        is_repository=True,
        branch=branch,
        is_clean=status == "" if status is not None else None,
        commit_count=commit_count,
        remote_url=remote_url,
    )


def _git(path: Path, *args: str) -> Optional[str]:
    try:
        completed = subprocess.run(
            ["git", "-C", str(path), *args], capture_output=True, text=True, check=False, timeout=5
        )
    except (FileNotFoundError, OSError, subprocess.TimeoutExpired):
        return None
    return completed.stdout.strip() if completed.returncode == 0 else None
