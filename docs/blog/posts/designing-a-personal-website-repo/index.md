---
date: 2026-07-15
title: "Designing a personal website repo"
tags:
  - meta
  - mkdocs
  - architecture
categories:
  - Meta
---

# Designing a personal website repo

This blog is built on a small idea: **set up the plumbing once, then make every
new post about the experiment — not the tooling.** This first post is a tour of
the repository that produces the site you are reading.

<!-- more -->

## Two tiers

The repo splits cleanly into two tiers:

- **Set up once (the CS part).** A tiny shared Python package, `avtsoof/`,
  exposes exactly three things — `REPO_ROOT`, `data_dir()`, and `save_fig()`.
  An editable install (`pip install -e .`) makes it importable from any post,
  from any working directory. It is written once and then left alone.
- **Per post (the fun part).** A post is a self-contained folder under
  `docs/blog/posts/<slug>/`: an `index.md`, an optional `build.py`, and an
  `assets/` folder for generated charts. Starting a post is *copy the template
  folder, fill in the front matter, write the experiment.*

## Why it stays small

The payoff of a one-time toolkit is that the code you write **per post** does not
grow as the blog grows. The plumbing is paid for once; everything after that is
content.

--8<-- "blog/posts/designing-a-personal-website-repo/assets/plot.html"

## How a plot reaches the page

A post that needs an interactive figure keeps a short `build.py`:

```python
from avtsoof.common_utils import save_fig
fig = ...                      # the actual experiment
print(save_fig(fig, HERE / "assets" / "plot.html"))
```

`save_fig` writes an inline Plotly `<div>` (JavaScript pulled from a CDN, so the
file stays small and text-based) and returns a **stable** MkDocs snippet-include
line. You paste that line into `index.md` once; re-running `build.py` overwrites
the chart in place, but the line never changes. The raw data lives under a
git-ignored root `data/`, so only the lightweight rendered chart is committed.

## The guard rails

Two things keep the published site honest:

- `mkdocs build --strict` promotes every warning — a broken link, a missing
  snippet include, a page absent from the nav — into a hard error.
- A versioned `pre-push` hook runs that strict build automatically, but only when
  a push to `main` actually touches docs-affecting files. CI runs the same build
  as a backstop.

The result: writing a post is copying a folder and telling a story, while the
structure quietly guarantees the site still builds.
