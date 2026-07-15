---
name: git-lfs
description: Use before committing files that may be large or binary — checks staged files and adds Git LFS tracking so binaries never enter regular git history.
---

# Git LFS

Mandated as a pre-commit check: committed binaries go through Git LFS; raw
datasets stay git-ignored under `data/`.

## Check before committing

Run the helper on your staged changes:

```sh
python .agents/skills/git-lfs/scripts/check_lfs.py
```

It flags any staged file that is binary or large (default > 5 MB) and **not yet
LFS-tracked**, and exits non-zero so you can fix it before committing.

## Fix a flagged file

Add a pattern and track it, then re-stage:

```sh
git lfs track "*.parquet"      # writes the pattern into .gitattributes
git add .gitattributes <file>
```

## Notes

- Generated `*.html` plots are text (Plotly via CDN) → normal git, **not** LFS.
- Raw datasets under `data/` are git-ignored → never need LFS.
- Common binary patterns already tracked in `.gitattributes`: images, PDFs,
  `*.parquet`, `*.npy/.npz`, `*.h5`, `*.zip`, `*.mp4`.
