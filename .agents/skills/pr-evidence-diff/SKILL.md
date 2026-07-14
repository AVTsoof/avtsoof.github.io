---
name: pr-evidence-diff
description: Use when preparing PR context from git history and diffs, and you need evidence extraction with file and line mappings before writing final PR prose.
---

# PR Evidence Diff

## Overview

Build evidence artifacts from repository data only:

- changed files and focused hunks
- commit-subject intent signals
- unclear intent that needs user clarification

This skill does not own final PR narrative composition. Use `pr-orchestrator` after evidence is prepared.

## When to Use

- You need accurate PR evidence from `git diff` and `git log`.
- You need file/line references for meaningful logic shifts.
- You need explicit "pending clarification" items where intent is not supported by commit history.

Do not use this skill to perform code review findings. Use `local-pr-review` for review output.

## Data Retrieval

Default target branch: `main`.

1. `git diff --unified=0 <target>..HEAD`
2. `git log <target>..HEAD --oneline`

Read repository files only when needed to interpret ambiguous hunks.

## Rules

- "Why" must come from commit messages only.
- If intent is not explained by commit history, mark as clarification needed.
- Prefer file-level relative links for all changed files.
- Add line-specific references only for important logic shifts.
- Keep evidence output concise and structured for downstream PR writing.

## Evidence Output Contract

Produce these sections:

1. `Overview Evidence`
   - one-line "what changed" from diff shape
   - one-line "why signals" from commit subjects
2. `Change Buckets`
   - group by top-level type (Features, Bugfixes, Refactors, Docs, Chores)
   - per subject: file list with short notes
3. `Pending Clarification`
   - list files/diffs where commit history does not explain intent
   - include direct clarification prompt text
4. `Potential Impact`
   - breaking changes, API shifts, dependencies, migrations

## Completion Checklist

- Diff and log were collected from the same target range.
- Every changed file appears in at least one change bucket.
- Why-statements are traceable to commit subjects.
- Ambiguous intent is listed under pending clarification.
- Output is evidence-focused and ready for `pr-orchestrator`.
