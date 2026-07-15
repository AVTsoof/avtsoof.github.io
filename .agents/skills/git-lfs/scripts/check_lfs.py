#!/usr/bin/env python3
"""Pre-commit check: flag staged files that should be tracked by Git LFS.

A staged file is flagged when it is binary or large (default > 5 MB) and is not
already covered by a Git LFS filter in ``.gitattributes``. Exits non-zero if any
file is flagged so the commit can be fixed first.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

DEFAULT_MAX_BYTES = 5 * 1024 * 1024  # 5 MB
BINARY_SNIFF_BYTES = 8192


def _git(*args: str) -> str:
    """Run a git command and return its stripped stdout."""
    result = subprocess.run(
        ["git", *args],
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.strip()


def staged_files() -> list[Path]:
    """Return added/modified staged files (deletions excluded)."""
    out = _git("diff", "--cached", "--name-only", "--diff-filter=AM")
    return [Path(line) for line in out.splitlines() if line]


def is_lfs_tracked(path: Path) -> bool:
    """True if the path is covered by an LFS filter in .gitattributes."""
    out = _git("check-attr", "filter", "--", str(path))
    # Format: "<path>: filter: lfs"
    return out.rsplit(":", 1)[-1].strip() == "lfs"


def is_binary(path: Path) -> bool:
    """Heuristic: a file is binary if its first chunk contains a NUL byte."""
    try:
        chunk = path.read_bytes()[:BINARY_SNIFF_BYTES]
    except OSError:
        return False
    return b"\x00" in chunk


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--max-bytes",
        type=int,
        default=DEFAULT_MAX_BYTES,
        help=f"size threshold in bytes (default {DEFAULT_MAX_BYTES})",
    )
    args = parser.parse_args()

    flagged: list[tuple[Path, str]] = []
    for path in sorted(staged_files()):
        if not path.is_file() or is_lfs_tracked(path):
            continue
        size = path.stat().st_size
        if size > args.max_bytes:
            flagged.append((path, f"large ({size} bytes)"))
        elif is_binary(path):
            flagged.append((path, "binary"))

    if not flagged:
        return 0

    print("Files that should be tracked by Git LFS before committing:", file=sys.stderr)
    for path, reason in flagged:
        print(f"  {path}  [{reason}]", file=sys.stderr)
    print(
        '\nFix: git lfs track "<pattern>" && git add .gitattributes <file>',
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
