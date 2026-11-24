"""Safe local Git metadata collection."""

from __future__ import annotations

import re
import subprocess
from pathlib import Path
from typing import Optional
from urllib.parse import urlsplit, urlunsplit

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
        remote_url=_sanitize_remote_url(remote_url) if remote_url else None,
    )


def _sanitize_remote_url(remote_url: str) -> str:
    """Remove URL user-info and query/fragment data before displaying a remote.

    Git remotes can contain embedded passwords, access tokens, or signed query
    parameters. Those values must not be copied into terminal or JSON reports.
    """
    if "://" in remote_url:
        parsed = urlsplit(remote_url)
        if parsed.scheme and parsed.netloc:
            host = parsed.hostname or ""
            if ":" in host and not host.startswith("["):
                host = "[{0}]".format(host)
            try:
                port = parsed.port
            except ValueError:
                port = None
            netloc = "{0}:{1}".format(host, port) if port is not None else host
            return urlunsplit((parsed.scheme, netloc, parsed.path, "", ""))

    # SCP-style Git remotes may also contain user-info, e.g. user:token@host:path.
    return re.sub(r"^[^/@]+@", "", remote_url)


def _git(path: Path, *args: str) -> Optional[str]:
    try:
        completed = subprocess.run(
            ["git", "-C", str(path), *args], capture_output=True, text=True, check=False, timeout=5
        )
    except (FileNotFoundError, OSError, subprocess.TimeoutExpired):
        return None
    return completed.stdout.strip() if completed.returncode == 0 else None
