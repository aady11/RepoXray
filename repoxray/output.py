"""Human-friendly terminal presentation without third-party dependencies."""

from __future__ import annotations

import os
import sys
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

from .models import GitInfo, HealthReport, LargeFile, ScanResult, SecretFinding
from .scanner import format_size


class Terminal:
    """Minimal ANSI styling that respects redirected output and NO_COLOR."""

    def __init__(self, color: Optional[bool] = None) -> None:
        self.color = color if color is not None else sys.stdout.isatty() and not os.environ.get("NO_COLOR")
        self.encoding = sys.stdout.encoding or "utf-8"
        try:
            "╭─│█✓⚠".encode(self.encoding)
            self.unicode = True
        except UnicodeEncodeError:
            self.unicode = False

    def style(self, text: str, code: str) -> str:
        return "\033[{0}m{1}\033[0m".format(code, text) if self.color else text

    def heading(self, text: str) -> str:
        return self.style(text, "1;36")

    def good(self, text: str) -> str:
        return self.style(text, "32")

    def warn(self, text: str) -> str:
        return self.style(text, "33")

    def bad(self, text: str) -> str:
        return self.style(text, "31")

    def dim(self, text: str) -> str:
        return self.style(text, "2")

    def sanitize(self, text: str) -> str:
        """Adapt display glyphs to legacy Windows console encodings."""
        if not self.unicode:
            text = text.translate(str.maketrans({
                "╭": "+", "╮": "+", "╰": "+", "╯": "+", "─": "-", "│": "|",
                "├": "+", "└": "+", "…": "...", "█": "#", "✓": "OK", "⚠": "!",
            }))
        return text.encode(self.encoding, errors="replace").decode(self.encoding)


def render_report(
    scan: ScanResult,
    languages: Dict[str, Dict[str, int]],
    largest: Sequence[LargeFile],
    large_files: Sequence[LargeFile],
    secrets: Sequence[SecretFinding],
    git: GitInfo,
    health: HealthReport,
    terminal: Terminal,
    show_tree: Optional[str] = None,
    focus: Optional[str] = None,
) -> str:
    """Render an overview plus optional focused sections."""
    sections = [_banner(terminal), _overview(scan, terminal)]
    if show_tree:
        sections.append(_section("Project tree", show_tree, terminal))
    if focus not in {"tree", "health", "secrets"}:
        sections.extend([
            _languages(languages, terminal), _files(largest, large_files, terminal),
            _git(git, terminal), _health(health, terminal), _secrets(secrets, terminal),
        ])
    elif focus == "health":
        sections.append(_health(health, terminal, include_rules=True))
    elif focus == "secrets":
        sections.append(_secrets(secrets, terminal))
    return "\n\n".join(section for section in sections if section)


def _banner(terminal: Terminal) -> str:
    width = 58
    return "\n".join([
        terminal.heading("╭" + "─" * width + "╮"),
        terminal.heading("│" + "RepoXray".center(width) + "│"),
        terminal.dim("│" + "X-ray vision for your Git repository".center(width) + "│"),
        terminal.heading("╰" + "─" * width + "╯"),
    ])


def _overview(scan: ScanResult, terminal: Terminal) -> str:
    rows = [
        ("Repository", str(scan.root)), ("Files", str(scan.file_count)),
        ("Directories", str(scan.directory_count)), ("Size", format_size(scan.size_bytes)),
        ("Hidden files", str(scan.hidden_file_count)), ("Ignored paths", str(len(scan.ignored_paths))),
    ]
    return _section("Repository", _key_values(rows), terminal)


def _languages(languages: Dict[str, Dict[str, int]], terminal: Terminal) -> str:
    if not languages:
        return _section("Languages", terminal.dim("No recognized source languages."), terminal)
    rows = []
    for language, values in list(languages.items())[:8]:
        percent = values["percentage"]
        rows.append("{0:<16} {1:<20} {2:>5.1f}%  ({3} files)".format(language, "█" * max(1, round(percent / 5)), percent, values["files"]))
    return _section("Languages", "\n".join(rows), terminal)


def _files(largest: Sequence[LargeFile], large_files: Sequence[LargeFile], terminal: Terminal) -> str:
    if not largest:
        return ""
    heading = "⚠ Large files" if large_files else "Largest files"
    lines = ["{0:>10}  {1}".format(format_size(file.size_bytes), file.path) for file in largest]
    note = "Threshold matches {0} file(s).".format(len(large_files)) if large_files else "No files exceed the large-file threshold."
    return _section(heading, "\n".join(lines + [terminal.dim(note)]), terminal)


def _git(git: GitInfo, terminal: Terminal) -> str:
    if not git.is_repository:
        return _section("Git", terminal.warn("Not a local Git repository."), terminal)
    status = "clean" if git.is_clean else "has uncommitted changes"
    rows = [("Branch", git.branch or "detached HEAD"), ("Working tree", status), ("Commits", str(git.commit_count or 0))]
    if git.remote_url:
        rows.append(("Remote", git.remote_url))
    return _section("Git", _key_values(rows), terminal)


def _health(health: HealthReport, terminal: Terminal, include_rules: bool = False) -> str:
    score_color = terminal.good if health.score >= 75 else terminal.warn if health.score >= 50 else terminal.bad
    lines = [score_color("{0}/100".format(health.score))]
    lines.extend(terminal.good("✓ " + item) for item in health.positives)
    lines.extend(terminal.warn("⚠ " + item) for item in health.warnings)
    if include_rules:
        lines.append(terminal.dim("Scoring rules:"))
        lines.extend(terminal.dim("  {0:+}  {1}".format(int(rule["points"]), rule["description"])) for rule in health.rules)
    lines.append(terminal.dim("Heuristic score only; it is not a scientific quality measurement."))
    return _section("Repo Health", "\n".join(lines), terminal)


def _secrets(secrets: Sequence[SecretFinding], terminal: Terminal) -> str:
    if not secrets:
        message = terminal.good("✓ No obvious secrets found")
    else:
        lines: List[str] = []
        for finding in secrets:
            location = finding.path + (":{0}".format(finding.line) if finding.line else "")
            stylize = terminal.bad if finding.severity == "HIGH" else terminal.warn
            lines.append(stylize("[{0}] {1} in {2}".format(finding.severity, finding.message, location)))
        message = "\n".join(lines)
    return _section("Sensitive-content scan", message + "\n" + terminal.dim("Local heuristic scan only; values are never shown or sent anywhere."), terminal)


def _key_values(rows: Iterable[Tuple[str, str]]) -> str:
    return "\n".join("{0:<16} {1}".format(label, value) for label, value in rows)


def _section(title: str, body: str, terminal: Terminal) -> str:
    return terminal.heading(title + "\n" + "─" * len(title)) + "\n" + body
