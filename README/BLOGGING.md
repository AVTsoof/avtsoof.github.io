# Blogging Guide

How to write a post in this repo — for both the author and the agent. A post is
a self-contained folder; the shared `avtsoof/` toolkit does the plumbing.

## New post

1. Copy `docs/blog/posts/_template/` → `docs/blog/posts/<slug>/` (lowercase,
   hyphenated).
2. Fill the front matter: `date`, `title`, `tags`, `categories`.
3. Glance at existing `docs/blog/posts/*/index.md` titles first to avoid
   repeating a topic.

The **Material blog plugin** auto-builds the index/archive/categories/tags from
each post's `date`. There is no registry to keep in sync.

## Plots (optional)

Write a short `build.py` in the post folder that focuses on the experiment and
delegates saving to the toolkit:

```python
from pathlib import Path
import plotly.express as px
from avtsoof.common_utils import data_dir, save_fig

HERE = Path(__file__).parent

def main() -> None:
    df = ...                          # load from data_dir("<name>")
    fig = px.line(df, x=..., y=...)   # the actual experiment
    print(save_fig(fig, HERE / "assets" / "plot.html"))

if __name__ == "__main__":
    main()
```

Run `python build.py` locally; `save_fig` writes `assets/plot.html` (inline
`<div>`, Plotly via CDN) and prints a **stable** snippet-include line — e.g.
`--8<-- "blog/posts/<slug>/assets/plot.html"`. Paste it into `index.md` **once**;
it never changes on re-runs. Commit the generated `assets/*.html` (raw data is
git-ignored, so plots must be built locally and committed for CI to find them).

## Data

Raw/large datasets live under git-ignored root `data/`, reached via
`avtsoof.common_utils.data_dir(name)`. **Never** commit raw data under `docs/`.

## Toolkit

Import shared helpers from `avtsoof.common_utils`. Promote a helper into
`avtsoof/` only when a *second* post needs it.

## Site boundaries

MkDocs builds only `docs/`. `*.py`, `superpowers/`, and `blog/posts/_template/`
are excluded from the built site (see `mkdocs.yml` `exclude_docs`). Run
`mkdocs build --strict` before pushing docs-affecting changes.
