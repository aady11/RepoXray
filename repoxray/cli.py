"""Command-line interface for RepoXray."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Optional, Sequence

from . import __version__
from .analyzer import detect_languages
from .gitinfo import inspect_git_repository
from .health import calculate_health
from .output import Terminal, render_report
from .scanner import RepositoryScanner, extension_breakdown, find_large_files, largest_files
from .secrets import scan_for_secrets
from .tree import build_tree


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI parser independently so it is easy to test."""
    parser = argparse.ArgumentParser(prog="repoxray", description="X-ray vision for a local repository. Everything stays on your machine.")
    parser.add_argument("path", nargs="?", default=".", help="Repository directory to scan (default: current directory).")
    parser.add_argument("--json", action="store_true", help="Print the full report as machine-readable JSON.")
    parser.add_argument("--secrets", action="store_true", help="Show only the sensitive-content scan.")
    parser.add_argument("--tree", action="store_true", help="Show a compact project tree.")
    parser.add_argument("--health", action="store_true", help="Show the health score and its scoring rules.")
    parser.add_argument("--include-ignored", action="store_true", help="Include standard generated directories in the scan.")
    parser.add_argument("--max-depth", type=_positive_int, default=4, help="Maximum tree depth (default: 4).")
    parser.add_argument("--max-tree-entries", type=_positive_int, default=80, help="Maximum tree entries (default: 80).")
    parser.add_argument("--large-file-threshold-mb", type=_positive_float, default=5.0, help="Large file threshold in MiB (default: 5).")
    parser.add_argument("--no-color", action="store_true", help="Disable ANSI terminal colors.")
    parser.add_argument("--version", action="version", version="repoxray {0}".format(__version__))
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    """Run RepoXray and return a conventional shell exit code."""
    args = build_parser().parse_args(argv)
    try:
        scan = RepositoryScanner(Path(args.path), include_ignored=args.include_ignored).scan()
    except (FileNotFoundError, NotADirectoryError) as error:
        print("repoxray: {0}".format(error), file=sys.stderr)
        return 2
    languages = detect_languages(scan)
    large_files = find_large_files(scan, int(args.large_file_threshold_mb * 1024 * 1024))
    secret_findings = scan_for_secrets(scan.files)
    git = inspect_git_repository(scan.root)
    health = calculate_health(scan, git, secret_findings, large_files)
    tree = build_tree(scan.root, include_ignored=args.include_ignored, max_depth=args.max_depth, max_entries=args.max_tree_entries) if args.tree else None
    if args.json:
        print(json.dumps(_report_dict(scan, languages, large_files, secret_findings, git, health, tree), indent=2, sort_keys=True))
        return 0
    focus = "tree" if args.tree and not (args.secrets or args.health) else "secrets" if args.secrets else "health" if args.health else None
    terminal = Terminal(color=False if args.no_color else None)
    report = render_report(scan, languages, largest_files(scan), large_files, secret_findings, git, health, terminal, tree, focus)
    print(terminal.sanitize(report))
    return 0


def _report_dict(scan: Any, languages: Dict[str, Dict[str, int]], large_files: Any, secrets: Any, git: Any, health: Any, tree: Optional[str]) -> Dict[str, Any]:
    report = scan.to_dict()
    report.update({
        "extensions": extension_breakdown(scan), "languages": languages,
        "largest_files": [file.to_dict() for file in largest_files(scan)],
        "large_files": [file.to_dict() for file in large_files],
        "secrets": [finding.to_dict() for finding in secrets], "git": git.to_dict(), "health": health.to_dict(),
    })
    if tree is not None:
        report["tree"] = tree
    return report


def _positive_int(value: str) -> int:
    try:
        parsed = int(value)
    except ValueError as error:
        raise argparse.ArgumentTypeError("must be an integer") from error
    if parsed <= 0:
        raise argparse.ArgumentTypeError("must be greater than zero")
    return parsed


def _positive_float(value: str) -> float:
    try:
        parsed = float(value)
    except ValueError as error:
        raise argparse.ArgumentTypeError("must be a number") from error
    if parsed <= 0:
        raise argparse.ArgumentTypeError("must be greater than zero")
    return parsed
