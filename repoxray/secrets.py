"""Local, redacted heuristic checks for accidentally committed secrets."""

from __future__ import annotations

import re
from typing import Iterable, List, Sequence, Tuple

from .models import FileRecord, SecretFinding


MAX_FILE_BYTES = 1_000_000
SENSITIVE_FILENAMES = {
    ".env",
    ".env.local",
    ".env.production",
    ".env.development",
    "id_rsa",
    "id_dsa",
    "credentials.json",
    "service-account.json",
}
SENSITIVE_SUFFIXES = (".pem", ".key", ".p12", ".pfx")
PLACEHOLDER_VALUES = {"", "changeme", "change-me", "example", "placeholder", "your-token", "your_api_key"}

PATTERNS: Sequence[Tuple[str, str, str, re.Pattern[str]]] = (
    ("HIGH", "private key", "possible private key material", re.compile(r"-----BEGIN (?:[A-Z ]+ )?PRIVATE KEY-----")),
    ("HIGH", "AWS access key", "possible AWS access key", re.compile(r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b")),
    ("HIGH", "GitHub token", "possible GitHub token", re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{20,}\b")),
    (
        "HIGH",
        "API key",
        "possible API key assignment",
        re.compile(r"\b(?:api[_-]?key|secret[_-]?key|access[_-]?token|auth[_-]?token)\b\s*[:=]\s*[\"']?([^\s\"'#]{8,})", re.IGNORECASE),
    ),
    (
        "MEDIUM",
        "password",
        "possible password assignment",
        re.compile(r"\b(?:password|passwd|pwd)\b\s*[:=]\s*[\"']?([^\s\"'#]{6,})", re.IGNORECASE),
    ),
)


def scan_for_secrets(files: Iterable[FileRecord]) -> List[SecretFinding]:
    """Inspect text-like local files and return redacted heuristic findings."""
    findings: List[SecretFinding] = []
    for file in files:
        findings.extend(_sensitive_filename_findings(file))
        if file.size_bytes <= MAX_FILE_BYTES:
            findings.extend(_scan_file(file))
    return _deduplicate(findings)


def _sensitive_filename_findings(file: FileRecord) -> List[SecretFinding]:
    name = file.path.name.lower()
    if name in SENSITIVE_FILENAMES or name.endswith(SENSITIVE_SUFFIXES):
        return [
            SecretFinding("MEDIUM", "sensitive file", file.relative_path, None, "sensitive filename should not usually be committed")
        ]
    return []


def _scan_file(file: FileRecord) -> List[SecretFinding]:
    try:
        content = file.path.read_text(encoding="utf-8", errors="replace")
    except (OSError, UnicodeError):
        return []
    if "\x00" in content:
        return []

    findings: List[SecretFinding] = []
    for line_number, line in enumerate(content.splitlines(), start=1):
        for severity, category, message, pattern in PATTERNS:
            match = pattern.search(line)
            if match is None or _is_placeholder(match):
                continue
            findings.append(SecretFinding(severity, category, file.relative_path, line_number, message))
    return findings


def _is_placeholder(match: re.Match[str]) -> bool:
    if not match.lastindex:
        return False
    return match.group(1).strip().lower() in PLACEHOLDER_VALUES


def _deduplicate(findings: List[SecretFinding]) -> List[SecretFinding]:
    unique = {}
    for finding in findings:
        unique[(finding.severity, finding.category, finding.path, finding.line)] = finding
    severity_rank = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
    return sorted(unique.values(), key=lambda item: (severity_rank.get(item.severity, 3), item.path, item.line or 0))
