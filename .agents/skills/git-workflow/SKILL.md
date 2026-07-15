---
name: git-workflow
description: Use when committing, branching, or integrating work — covers atomic commits, commit messages, build integrity, the spec-branch + `--no-ff` merge rule, and the pre-push strict-build gate.
---

# Git Workflow

## Methodology

- Trunk-based development: branches are short-lived and merge back frequently.
- **The Golden Rule:** local history is a "Save Point" (messy allowed); shared
  history is a "Story" (must be curated).

## Spec-driven work

- Changes implemented from a spec/design file are done on a dedicated branch
  (e.g. `feat/<topic>`) as atomic commits.
- Integrate to `main` with `git merge --no-ff` (preserve the feature boundary).

## Atomic commits

- **One logic, one commit:** a commit is a single complete logical change.
- **Concept over component:** never split one logical change across commits;
  commit the entire vertical slice.
- **Revert/bisect safe:** every commit is reversible in isolation and leaves the
  repo buildable.
- **Stash-Test-Verify:** when splitting, ensure unstaged changes are not required
  for the build (`git stash --keep-index` to verify).
- Never `git add .` for phase commits — stage explicit paths.

## Commit messages

- Subject ≤ 50 chars, body wrapped at 72, separated by a blank line.
- Imperative mood ("Fix bug", not "Fixed bug").
- The body explains the *why* (context/architecture), not the *what* (diff).

## Workflow hygiene

- Prefix incomplete work `WIP:`; never merge WIP to `main`.
- Use `git commit --fixup <hash>` instead of "fix typo" commits, then
  `git rebase -i --autosquash` to consolidate before pushing.

## Build integrity & the pre-push gate

- Every commit in shared history must build and pass tests.
- `mkdocs build --strict` renders the site and promotes warnings to hard errors
  (broken links, `nav` mismatches, missing `--8<--` snippet includes). Run it on
  any commit that touches `docs/`, `mkdocs.yml`, or generated assets.
- A versioned pre-push gate automates this: `.githooks/pre-push` (git-required
  entrypoint) execs `.githooks/pre-push-main`, which runs `mkdocs build --strict`
  **only** when a push updates `main` **and** touches docs-affecting paths.
  Activated once per clone via `git config core.hooksPath .githooks` (wired into
  `bootstrap.py`). Bypass a false positive with `git push --no-verify`;
  remote CI runs the same strict build as a backstop.
