"""Tiny shared helpers: repo-root-anchored paths and a Plotly figure saver.

Kept deliberately small (paths + one figure-save helper). Promote a helper here
only when a second post genuinely needs it.
"""

from __future__ import annotations

from pathlib import Path


def _find_repo_root(marker: str = "pyproject.toml") -> Path:
    """Walk upward from this file until the repo-root marker is found."""
    for parent in Path(__file__).resolve().parents:
        if (parent / marker).is_file():
            return parent
    raise RuntimeError(f"repo-root marker {marker!r} not found above {__file__}")


REPO_ROOT: Path = _find_repo_root()
DOCS: Path = REPO_ROOT / "docs"


def data_dir(name: str) -> Path:
    """Return (creating if needed) the git-ignored datastore dir ``data/<name>``."""
    target = REPO_ROOT / "data" / name
    target.mkdir(parents=True, exist_ok=True)
    return target


def save_fig(fig, out: Path, height: str = "450px") -> str:
    """Write ``fig`` as an inline Plotly ``<div>`` and return a stable include line.

    The ``div_id`` is derived from the output filename, so an unchanged experiment
    reproduces a byte-identical file (no git churn). The returned MkDocs snippet
    line (``--8<-- "..."``) is pasted once into the post's ``index.md``.

    ``height`` is written as a concrete size on the wrapper so the container hugs
    the plot exactly; a percentage height would leave a gap before the next block.
    """
    out = Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.write_html(
        out,
        include_plotlyjs="cdn",
        full_html=False,
        div_id=out.stem,
        default_height=height,
    )
    return f'--8<-- "{out.relative_to(DOCS).as_posix()}"'
