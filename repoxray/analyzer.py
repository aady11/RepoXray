"""Language and file-type analysis."""

from __future__ import annotations

from collections import defaultdict
from typing import Dict

from .models import ScanResult


LANGUAGE_BY_EXTENSION = {
    ".py": "Python",
    ".pyi": "Python",
    ".js": "JavaScript",
    ".mjs": "JavaScript",
    ".cjs": "JavaScript",
    ".ts": "TypeScript",
    ".tsx": "TypeScript",
    ".jsx": "JavaScript",
    ".html": "HTML",
    ".htm": "HTML",
    ".css": "CSS",
    ".scss": "SCSS",
    ".sass": "Sass",
    ".less": "Less",
    ".java": "Java",
    ".kt": "Kotlin",
    ".kts": "Kotlin",
    ".go": "Go",
    ".rs": "Rust",
    ".c": "C",
    ".h": "C/C++ Header",
    ".cpp": "C++",
    ".cxx": "C++",
    ".cc": "C++",
    ".hpp": "C++ Header",
    ".cs": "C#",
    ".rb": "Ruby",
    ".php": "PHP",
    ".swift": "Swift",
    ".scala": "Scala",
    ".sh": "Shell",
    ".bash": "Shell",
    ".zsh": "Shell",
    ".ps1": "PowerShell",
    ".sql": "SQL",
    ".r": "R",
    ".dart": "Dart",
    ".lua": "Lua",
    ".ex": "Elixir",
    ".exs": "Elixir",
    ".erl": "Erlang",
    ".fs": "F#",
    ".fsx": "F#",
    ".vue": "Vue",
    ".svelte": "Svelte",
    ".md": "Markdown",
    ".rst": "reStructuredText",
    ".json": "JSON",
    ".yaml": "YAML",
    ".yml": "YAML",
    ".toml": "TOML",
    ".xml": "XML",
}


def detect_languages(scan: ScanResult) -> Dict[str, Dict[str, int]]:
    """Group recognized source files by byte count and file count."""
    totals: Dict[str, Dict[str, int]] = defaultdict(lambda: {"bytes": 0, "files": 0})
    for file in scan.files:
        language = LANGUAGE_BY_EXTENSION.get(file.extension)
        if language is None:
            continue
        totals[language]["bytes"] += file.size_bytes
        totals[language]["files"] += 1

    recognized_bytes = sum(values["bytes"] for values in totals.values())
    ordered = sorted(totals.items(), key=lambda item: (-item[1]["bytes"], item[0]))
    return {
        language: {
            "bytes": values["bytes"],
            "files": values["files"],
            "percentage": round(values["bytes"] * 100 / recognized_bytes, 1)
            if recognized_bytes
            else 0,
        }
        for language, values in ordered
    }
