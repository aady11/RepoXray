"""Data structures shared by RepoXray's analyzers."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass(frozen=True)
class FileRecord:
    """Metadata collected for one scanned file."""

    path: Path
    relative_path: str
    size_bytes: int
    extension: str
    is_hidden: bool

    def to_dict(self) -> Dict[str, Any]:
        return {
            "path": self.relative_path,
            "size_bytes": self.size_bytes,
            "extension": self.extension or "[no extension]",
            "hidden": self.is_hidden,
        }


@dataclass
class ScanResult:
    """Repository inventory produced by :class:`RepositoryScanner`."""

    root: Path
    files: List[FileRecord] = field(default_factory=list)
    directory_count: int = 0
    ignored_paths: List[str] = field(default_factory=list)

    @property
    def file_count(self) -> int:
        return len(self.files)

    @property
    def size_bytes(self) -> int:
        return sum(file.size_bytes for file in self.files)

    @property
    def hidden_file_count(self) -> int:
        return sum(file.is_hidden for file in self.files)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "repository": str(self.root),
            "files": self.file_count,
            "directories": self.directory_count,
            "size_bytes": self.size_bytes,
            "hidden_files": self.hidden_file_count,
            "ignored_paths": self.ignored_paths,
        }


@dataclass(frozen=True)
class LargeFile:
    """A scanned file exceeding the configured large-file threshold."""

    path: str
    size_bytes: int

    def to_dict(self) -> Dict[str, Any]:
        return {"path": self.path, "size_bytes": self.size_bytes}


@dataclass(frozen=True)
class SecretFinding:
    """A local, value-redacted sensitive-content finding."""

    severity: str
    category: str
    path: str
    line: Optional[int]
    message: str

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {
            "severity": self.severity,
            "category": self.category,
            "path": self.path,
            "message": self.message,
        }
        if self.line is not None:
            result["line"] = self.line
        return result


@dataclass(frozen=True)
class GitInfo:
    """Useful local Git metadata, when the target is a Git repository."""

    is_repository: bool
    branch: Optional[str] = None
    is_clean: Optional[bool] = None
    commit_count: Optional[int] = None
    remote_url: Optional[str] = None
    error: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "is_repository": self.is_repository,
            "branch": self.branch,
            "is_clean": self.is_clean,
            "commit_count": self.commit_count,
            "remote_url": self.remote_url,
            "error": self.error,
        }


@dataclass
class HealthReport:
    """Transparent, heuristic repository health result."""

    score: int
    positives: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    rules: List[Dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "score": self.score,
            "positives": self.positives,
            "warnings": self.warnings,
            "rules": self.rules,
            "disclaimer": "Heuristic score only; it is not a scientific quality measurement.",
        }
