"""Filesystem inventory for local repositories."""

from __future__ import annotations

import os
from collections import Counter
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence

from .models import FileRecord, LargeFile, ScanResult


DEFAULT_IGNORED_NAMES = frozenset(
    {
        ".git",
        ".next",
        "__pycache__",
        "node_modules",
        ".venv",
        "venv",
        "dist",
        "build",
        ".mypy_cache",
        ".pytest_cache",
        ".tox",
        ".nox",
        ".coverage",
    }
)


class RepositoryScanner:
    """Recursively collect lightweight metadata without reading file contents."""

    def __init__(
        self,
        root: Path,
        ignored_names: Optional[Iterable[str]] = None,
        include_ignored: bool = False,
    ) -> None:
        self.root = root.expanduser().resolve()
        self.ignored_names = set(ignored_names or DEFAULT_IGNORED_NAMES)
        self.include_ignored = include_ignored

    def scan(self) -> ScanResult:
        """Return an inventory of regular, readable files under ``root``."""
        if not self.root.exists():
            raise FileNotFoundError("Repository path does not exist: {0}".format(self.root))
        if not self.root.is_dir():
            raise NotADirectoryError("Repository path is not a directory: {0}".format(self.root))

        result = ScanResult(root=self.root)
        for directory, directory_names, file_names in os.walk(
            self.root, topdown=True, followlinks=False
        ):
            current = Path(directory)
            kept_directories = []
            for name in sorted(directory_names):
                child = current / name
                if not self.include_ignored and name in self.ignored_names:
                    result.ignored_paths.append(child.relative_to(self.root).as_posix())
                    continue
                kept_directories.append(name)
            directory_names[:] = kept_directories

            if current != self.root:
                result.directory_count += 1

            for name in sorted(file_names):
                candidate = current / name
                try:
                    if not candidate.is_file() or candidate.is_symlink():
                        continue
                    stat = candidate.stat()
                except OSError:
                    continue
                relative = candidate.relative_to(self.root).as_posix()
                result.files.append(
                    FileRecord(
                        path=candidate,
                        relative_path=relative,
                        size_bytes=stat.st_size,
                        extension=candidate.suffix.lower(),
                        is_hidden=any(part.startswith(".") for part in candidate.relative_to(self.root).parts),
                    )
                )
        return result


def extension_breakdown(scan: ScanResult) -> Dict[str, int]:
    """Return file counts grouped by normalized file extension."""
    counts = Counter(file.extension or "[no extension]" for file in scan.files)
    return dict(sorted(counts.items(), key=lambda item: (-item[1], item[0])))


def find_large_files(scan: ScanResult, threshold_bytes: int) -> List[LargeFile]:
    """Return threshold-exceeding files, largest first."""
    return [
        LargeFile(path=file.relative_path, size_bytes=file.size_bytes)
        for file in sorted(scan.files, key=lambda item: item.size_bytes, reverse=True)
        if file.size_bytes >= threshold_bytes
    ]


def largest_files(scan: ScanResult, limit: int = 8) -> List[LargeFile]:
    """Return the largest scanned files, regardless of threshold."""
    return [
        LargeFile(path=file.relative_path, size_bytes=file.size_bytes)
        for file in sorted(scan.files, key=lambda item: item.size_bytes, reverse=True)[:limit]
    ]


def format_size(size_bytes: int) -> str:
    """Format a byte count for terminal output."""
    units: Sequence[str] = ("B", "KB", "MB", "GB", "TB")
    value = float(size_bytes)
    for unit in units:
        if value < 1024 or unit == units[-1]:
            return "{0:.1f} {1}".format(value, unit) if unit != "B" else "{0} B".format(int(value))
        value /= 1024
    return "{0:.1f} TB".format(value)
