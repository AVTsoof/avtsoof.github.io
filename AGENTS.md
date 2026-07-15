# AGENTS.md — Repo Rules & Governance

Lean index for `avtsoof.github.io` (MkDocs personal portfolio + research blog).
This file holds only the structure skeleton, a few invariants, and a pointer
table. **All detail lives in the skills under `.agents/skills/`.**

## Directory skeleton

```text
avtsoof.github.io/
├── AGENTS.md                 # this file
├── README.md                 # project overview + setup (entry point)
├── README/                   # long-form guides (e.g. BLOGGING.md)
├── .githooks/                # versioned hooks (pre-push strict-build gate)
├── .agents/skills/           # thin skills (see pointer table)
├── avtsoof/                  # shared Python toolkit (pip install -e .)
├── pyproject.toml            # makes `avtsoof` importable
├── data/                     # root datastore — GIT-IGNORED
├── docs/                     # MkDocs source (public site)
│   ├── index.md · about.md
│   ├── blog/posts/<slug>/    # self-contained posts (index.md, build.py, assets/)
│   └── superpowers/          # specs/plans — EXCLUDED from the site
├── mkdocs.yml
└── requirements.txt
```

*Update this skeleton only when the folder **structure** changes — never as
content grows.*

## Invariants

- **R1 — Posts are self-contained folders:** each post lives in
  `docs/blog/posts/<slug>/` (lowercase, hyphenated) with its `index.md`, optional
  `build.py`, and `assets/`. *(Detail: `README/BLOGGING.md`.)*
- **R2 — Root datastore:** all raw/binary datasets live under root `data/`, which
  is fully git-ignored; never commit raw data under `docs/`. *(Detail:
  `README/BLOGGING.md`.)*
- **R3 — Delegation:** load the skill that owns a task before acting; keep this
  file lean — when in doubt, a rule belongs in a skill, not here.

## Pointer table

| Task | Skill |
| --- | --- |
| Git methodology, atomic commits, branch + `--no-ff` merge, pre-push gate | `git-workflow` |
| `.gitignore` scope, security, syntax | `gitignore` |
| Language-agnostic clean code / SRP / robustness | `clean-code` |
| Python style (pathlib, argparse, typing) | `python-style` |
| Authoring/splitting skills (minimalism) | `skill-authoring` |
| Writing a blog post (template, plots, data, boundaries) | `README/BLOGGING.md` |
| Large/binary files before commit | `git-lfs` |
