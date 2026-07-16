# avtsoof.github.io

Personal portfolio and research blog, built with [MkDocs](https://www.mkdocs.org/)
and [Material](https://squidfunk.github.io/mkdocs-material/), and published to
GitHub Pages.

## Setup

```bash
# Windows / macOS / Linux
python bootstrap.py
```

This creates a `.venv`, installs dependencies (including the editable `avtsoof`
toolkit via `pip install -e .`), and wires the versioned git hooks
(`core.hooksPath .githooks`).

If a `.venv` already exists, the script asks whether to recreate it or install
on top of it. Pass `--override` to recreate it without prompting:

```bash
python bootstrap.py --override
```

## Project extras

Sub-projects can declare extra dependencies in `projects/<slug>/requirements.txt`.
Install them into the root `.venv` with:

```bash
python bootstrap.py --project <slug>
```

## Local preview

```bash
.venv/Scripts/mkdocs serve      # Windows: .\.venv\Scripts\mkdocs serve
```

Open the printed local URL. Build the static site with `mkdocs build --strict`.

## Where things live

| Topic | File |
| --- | --- |
| Repo rules, structure, invariants, and skill index | `AGENTS.md` |
| How to write a blog post (template, plots, data) | `README/BLOGGING.md` |
| Task-specific conventions (git, style, LFS, …) | `.agents/skills/` |

Raw datasets default to the git-ignored root `data/` and are accessed from code
via `avtsoof.common_utils.data_dir(name)` (optionally overridden with
`AVTSOOF_DATA_DIR`); posts are self-contained folders under
`docs/blog/posts/<slug>/`.
