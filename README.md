# avtsoof.github.io

Personal portfolio and research blog, built with [MkDocs](https://www.mkdocs.org/)
+ [Material](https://squidfunk.github.io/mkdocs-material/) and published to GitHub
Pages.

## Setup

```powershell
# Windows
.\setup.ps1
```

```bash
# macOS / Linux
./setup.sh
```

This creates a `.venv`, installs dependencies (including the editable `avtsoof`
toolkit via `pip install -e .`), and wires the versioned git hooks
(`core.hooksPath .githooks`).

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

Raw datasets live under the git-ignored root `data/`; posts are self-contained
folders under `docs/blog/posts/<slug>/`.
