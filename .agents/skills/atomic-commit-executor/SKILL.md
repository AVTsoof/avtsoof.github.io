---
name: atomic-commit-executor
description: Use when implementing or refactoring with local git commits and you need strict phase-by-phase atomic commits with targeted validation before each commit.
---

# Atomic Commit Executor

## Overview

Execute local changes as small, reviewable commits with one logical purpose per phase.

This skill owns execution discipline (edit, test, stage, commit). It does not own commit regroup analysis.

## When to Use

- You already know the desired change and need to commit in clean phases.
- You need explicit file-by-file staging and commit boundaries.
- You want targeted tests per phase before commit.

Do not use this skill for branch-level regroup/cherry-pick planning. Use `commit-regroup` for that.

## Hard Constraints

- Never use `git add .` for phase commits.
- Never combine unrelated changes in the same commit.
- Never use destructive git commands unless explicitly requested.
- Never push from this workflow.
- If tests fail in a phase, fix inside that phase before commit.

## Workflow

1. Inspect current state:
   - `git status --short`
   - map touched files to the current phase objective
2. Implement only the current phase scope.
3. Run targeted validation for touched area.
4. Stage only phase files by explicit path.
5. Commit with scoped conventional subject.
6. Repeat for next phase.

## Suggested Phase Subjects

- `refactor(<scope>): <atomic change>`
- `feat(<scope>): <atomic change>`
- `fix(<scope>): <atomic change>`
- `test(<scope>): <test-only atomic change>`
- `chore(validation): <non-functional validation or polish>`

## Output Format

For each phase, report:

- `Phase`: objective
- `Files`: exact staged paths
- `Validation`: commands and pass/fail summary
- `Commit`: full commit subject
- `Next`: next phase objective

## Completion Checklist

- Every commit has one clear purpose.
- Each phase was validated before commit.
- Staging used explicit paths only.
- No unrelated files were committed.
- No pushes or history rewrites were performed.
