"""Compact, deterministic repository tree rendering."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable, List, Optional, Set

from .scanner import DEFAULT_IGNORED_NAMES


def build_tree(
    root: Path,
    ignored_names: Optional[Iterable[str]] = None,
    include_ignored: bool = False,
    max_depth: int = 4,
    max_entries: int = 80,
) -> str:
    """Return an intentionally bounded tree so large repositories stay readable."""
    root = root.expanduser().resolve()
    ignored = set(ignored_names or DEFAULT_IGNORED_NAMES)
    lines = [root.name or str(root)]
    emitted = [0]
    _append_children(root, "", lines, ignored, include_ignored, max_depth, max_entries, emitted, 0)
    if emitted[0] >= max_entries:
        lines.append("… tree truncated after {0} entries".format(max_entries))
    return "\n".join(lines)


def _append_children(
    directory: Path, prefix: str, lines: List[str], ignored: Set[str], include_ignored: bool,
    max_depth: int, max_entries: int, emitted: List[int], depth: int,
) -> None:
    if depth >= max_depth or emitted[0] >= max_entries:
        return
    try:
        children = sorted(
            [child for child in directory.iterdir() if include_ignored or child.name not in ignored],
            key=lambda child: (not child.is_dir(), child.name.lower()),
        )
    except OSError:
        return
    remaining = max_entries - emitted[0]
    visible = children[:remaining]
    for index, child in enumerate(visible):
        is_last = index == len(visible) - 1 and len(visible) == len(children)
        connector = "└── " if is_last else "├── "
        suffix = "/" if child.is_dir() else ""
        lines.append("{0}{1}{2}{3}".format(prefix, connector, child.name, suffix))
        emitted[0] += 1
        if child.is_dir():
            _append_children(
                child, prefix + ("    " if is_last else "│   "), lines, ignored, include_ignored,
                max_depth, max_entries, emitted, depth + 1,
            )
        if emitted[0] >= max_entries:
            return
    if len(children) > len(visible) and emitted[0] < max_entries:
        lines.append("{0}└── … {1} more entries".format(prefix, len(children) - len(visible)))
