---
name: commit-split
description: 'Split the current branch''s UNCOMMITTED working-tree changes into atomic, subject-based commits and stage + commit them one by one in dependency order. Groups by semantic subject (feature / fix / refactor / concept), NOT by file — a single file''s changes may be split across several commits at the hunk / line level. NEVER edits code, NEVER pushes. Use when user says "split my changes into commits", "commit these changes atomically", "make atomic commits", "stage and commit by subject", "break up my working changes", "commit hunk by hunk".'
argument-hint: '[commit message convention: conventional (default) | caveman-commit]'
---

# Commit Split

Take the messy pile of uncommitted changes on the current branch and turn it into a clean sequence of **atomic, subject-scoped commits**, committed in dependency order.

Grouping is by **semantic subject**, not by file. One file's changes can be split across multiple commits; staging happens at the **hunk / line level** so a single commit can contain only some lines of a file.

This is the working-tree counterpart to the read-only `commit-regroup` skill (which reorganizes already-committed history). This skill *creates commits*.

## When to Use

- Working tree has many unrelated changes mixed together and the user wants focused commits.
- User wants each commit to represent one feature / fix / refactor / concept.
- User wants dependency-correct commit order (a change that others build on gets committed first).
- User wants hunk-level control ("commit only these lines, not the whole file").

## Hard Constraints

- **NEVER edit, add, delete, or reformat code / file contents.** Only stage and commit changes that already exist in the working tree.
- **NEVER run** `git push`, `git reset --hard`, `git checkout -- <file>`, `git restore <file>` (without `--staged`), `git clean`, or anything that discards work.
- **NEVER `git commit --amend`** an existing commit or rewrite published history.
- Allowed git (mutating only in these ways): `add` / `add -p`, `apply --cached`, `restore --staged`, `commit` (new commits only), `stash` **only** with explicit user approval.
- Allowed git (read-only): `status`, `diff`, `log`, `show`, `rev-parse`, `branch`, `ls-files`.
- The total set of changes after all commits must equal the original working-tree state. **No line of the diff may be lost, altered, or invented.** Verify this at the end.

## Procedure

### 1. Safety & preconditions

1. `git rev-parse --abbrev-ref HEAD` → confirm branch; refuse if on a protected branch (e.g. `main`, `master`) and ask user to switch first.
2. `git status --porcelain` → confirm there ARE uncommitted changes. If none, stop and report.
3. If the index already has staged changes (`git diff --staged --stat` non-empty): stop and ask the user. Offer to unstage cleanly with `git restore --staged .` so grouping starts from a clean index (this does NOT touch file contents). Do not proceed until resolved.
4. Snapshot the starting state for the final integrity check: record `git diff HEAD` (full patch of everything, staged + unstaged, tracked) and the list of untracked files (`git ls-files --others --exclude-standard`).

### 2. Inventory the changes

- Tracked modifications: `git diff HEAD` — read the FULL diff, hunk by hunk.
- Untracked files: `git ls-files --others --exclude-standard`.
- For each hunk, read the surrounding code to understand *intent*, not just the text. Note the file and the line range.

### 3. Cluster hunks by subject

Group every hunk (and every untracked file) into **subjects** = one feature, one bugfix, or one introduced concept. Signals, in priority:

1. **Semantic intent** — same feature/fix/concept (primary).
2. **Code coupling** — a hunk that only makes sense because of another hunk.
3. **Path / module proximity** — reinforces, but does NOT force, grouping.

Rules:
- A hunk belongs to exactly one subject. If lines within one hunk serve two subjects, split the hunk (see staging techniques) so each subject gets only its lines.
- Grouping is by subject, **never** "one commit per file". Same file → multiple commits is expected and normal.
- Determine **dependencies**: if subject B's code references or relies on subject A's change, A must be committed first. Produce a topological order (dependencies first).
- Flag anything that looks like a leftover debug line, stray print, or unrelated edit. Changes you cannot confidently assign to a subject go into a **`misc` commit**:
  - By default the `misc` commit is placed **after** all subject commits.
  - **But** if a subject commit depends on a leftover change (won't build / won't make sense without it), move that change into a `misc` commit placed **before** the dependent commit(s).
- When subject grouping, dependency order, or a commit message is genuinely ambiguous, **ask the user a clarifying question** rather than guessing.

### 4. Present the plan and get approval

Before staging anything, show the user:

```
COMMIT SPLIT PLAN — <branch>  |  N subjects  |  commit order = dependency order

1. <type>(<scope>): <subject one-liner>
   - file_a.py: hunk @ Lx–Ly (what it does)
   - file_b.py: hunk @ Lp–Lq
   depends on: none
2. <type>(<scope>): <subject one-liner>
   - file_a.py: hunk @ Lm–Ln   # same file as commit 1, different lines
   depends on: commit 1
...
N. chore: misc  (leftover / unassigned changes)
   - placed AFTER subject commits by default; placed BEFORE any commit that depends on these leftovers
```

Wait for user confirmation (or edits to the grouping) before executing. Ask clarifying questions whenever grouping, order, or messages are ambiguous. If the user pre-approved execution, still print the plan first, then proceed.

### 5. Execute — one subject at a time, in dependency order

For each subject, in order:

1. **Stage only that subject's changes** (see staging techniques below). Nothing else.
2. **Verify the staged content**: `git diff --staged` — confirm it contains exactly the intended hunks/lines and nothing from other subjects.
3. **Commit** (new commit only, no push): `git commit -m "<message>"`. Use the message convention from the argument (default Conventional Commits; if `caveman-commit` requested, follow the `caveman-commit` skill).
4. Re-inspect remaining unstaged changes before moving to the next subject.

Never stage a later subject's lines "to save a step". Each commit stays atomic.

### Staging techniques (hunk / line level)

- **Whole file** (all its changes belong to one subject): `git add <file>`.
- **Untracked file** entirely in one subject: `git add <file>`. To stage only part of a new file: `git add -N <file>` then stage hunks.
- **Some hunks of a file**: `git add -p <file>` and answer `y`/`n` per hunk. If a hunk mixes subjects, use `s` to split it, or `e` to hand-edit the patch.
- **Non-interactive / precise line control** (preferred for automation): build a patch of just the wanted hunks and apply it to the index:
  ```bash
  git diff -- <file> > /tmp/subject.patch   # then trim to only the wanted hunks
  git apply --cached /tmp/subject.patch
  ```
  Keep each hunk's `@@` header and context lines intact when trimming, or `git apply` will reject it.
- **Undo a mis-stage** without touching files: `git restore --staged <file>` (safe; leaves working tree untouched).

### 6. Completion checks

- Every hunk / untracked file from step 2 landed in exactly one commit (leftovers in a `misc` commit, ordered correctly relative to any commit that depends on them).
- `git log --oneline <base>..HEAD` shows the new commits in dependency order.
- **Integrity**: after all commits, `git diff HEAD` against the *original* HEAD equals the snapshot from step 1 (no line added, dropped, or modified). If anything differs, report it — do not attempt to "fix" file contents.
- Working tree is clean (all changes committed, leftovers captured in the `misc` commit).
- No `git push` was run. No file contents were edited. No history was rewritten.

## Notes

- Atomic commits ideally each build/pass on their own; this skill does not run builds or edit code to achieve that. If a proposed split would leave an intermediate commit broken, note it in the plan and let the user decide.
- `git add -p` hunks can be coarser than a single line; use `s` (split) then `e` (edit) for true line-level control.
- Report, don't repair: if the working tree is in a surprising state, surface it and stop rather than guessing.
