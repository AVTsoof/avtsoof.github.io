---
name: local-pr-review
description: 'Review a local branch diff as if it were a PR — terse, actionable findings plus an intent/why/what/how/problems report. Use when asked to review a branch, review a diff, do a local PR review, or act as a code reviewer on local changes.'
argument-hint: '<headBranch> [baseBranch=main]'
---

# Local PR Review

Review the changes on the head branch (the feature branch to review) compared to the base branch (defaults to `main`). Use the branch names provided as arguments; if the base branch is omitted, assume `main`. If no head branch is given, use the current branch.

Treat it as a pull request and act as the reviewer.

## Scope

- Diff the two branches locally (use the merge-base: `git diff <base>...<head>`). Read the full diff and the surrounding code you need to understand it.
- **Only reflect on the changes**, not on pre-existing code from before this branch.
- If pre-existing code is what forced the author to make a change the way they did, **note that and give them slack** — flag it as a nit at most, not a blocker.

## Output

### 1. Intent & Summary (short narrative)

- **What** the branch does (the actual change).
- **Why** it was done (the problem it solves).
- **How** it was done (approach / key mechanisms), referencing the relevant files and functions.
- One honest line on overall direction.

### 2. Findings (terse, one line per finding)

Follow the caveman-review style — terse and actionable. One line per finding: location, problem, fix. No throat-clearing.

**Format:** `<file>:L<line>: <severity>: <problem>. <fix>.`

**Severity prefixes:**
- `🔴 bug:` — broken behavior, will cause an incident
- `🟡 risk:` — works but fragile (race, missing null check, swallowed error, magic number, latent trap)
- `🔵 nit:` — style, naming, micro-optim, dead code. Author can ignore
- `❓ q:` — genuine question, not a suggestion
- `✅ good:` — call out a notably good change (sparingly)

**Rules:**
- Exact line numbers, exact symbol names in backticks.
- Concrete fix, not "consider refactoring".
- Include the *why* only if it isn't obvious from the problem statement.
- Drop hedging ("perhaps", "maybe", "I think") — if unsure, use `q:`.
- Don't restate what the line does — the reader can read the diff.
- Distinguish **active bugs** from **latent/hypothetical** issues (say which). If something is safe today only because of an unrelated code path, say so and downgrade the severity.

**Auto-clarity exception:** For security findings (CVE-class), architectural disagreements, or where the author is new, write a normal paragraph with rationale, then resume terse.

### 3. Where to look hardest before merge

3–5 highest-priority items (the ones that can actually cause a crash, data corruption, or incorrect results), with file links.

### 4. Slack given

Briefly list the choices you did NOT penalize because pre-existing code / existing conventions forced them.

## Boundaries

Review only. Do not write the code fix, do not approve/request-changes, do not run linters. Output ready to paste into the PR.
