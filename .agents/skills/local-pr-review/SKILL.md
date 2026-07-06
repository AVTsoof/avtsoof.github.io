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
- Create a markdown report file at `tmp/local-pr-review-{source_branch}({short-commit-id})_{target_branch}({short-commit-id}).md`.

## Output

Write the final report as clean, readable Markdown.

- Use clear section headings in the same order as defined below.
- Use short paragraphs and bullet lists where they improve scanability.
- Keep line lengths reasonable and avoid dense text blocks.
- Use fenced code blocks only when showing commands or snippets.
- Keep terminology and severity labels consistent throughout the report.

### 1. Intent & Summary (short narrative)

- **What** the branch does (the actual change).
- **Why** it was done (the problem it solves).
- **How** it was done (approach / key mechanisms), referencing the relevant files and functions.
- One honest line on overall direction.
- Prefer a compact bullet list for this section (4-6 bullets total).

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
- Put the 3-5 highest-priority pre-merge checks first in this section (items most likely to cause crashes, data corruption, or incorrect results), each with file links.
- Note "slack given" inline in the relevant finding (typically as `🔵 nit:`), instead of using a separate section.
- Keep exactly one finding per line for fast scanning.

**Auto-clarity exception:** For security findings (CVE-class), architectural disagreements, or where the author is new, write a normal paragraph with rationale, then resume terse.

### 3. Architectural / Global notes (only when needed)

Only add this section for cross-cutting architectural observations or global constraints that do not fit a single finding.
Use concise bullet points in this section.

## Boundaries

Review only. Do not write the code fix, do not approve/request-changes, do not run linters. Output ready to paste into the PR.
