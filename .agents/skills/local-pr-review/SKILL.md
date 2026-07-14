---
name: local-pr-review
description: 'Review a local branch diff as if it were a PR — terse, actionable findings plus an intent/why/what/how/problems report. Use when asked to review a branch, review a diff, do a local PR review, or act as a code reviewer on local changes.'
argument-hint: '<headBranch> [baseBranch=main] [free-text intent/description] [--skip-tests | "skip tests" | "no pytest" | similar]'
---

# Local PR Review

Review head branch (feature branch) vs base branch (default `main`). Branch names come from arguments. Base omitted, assume `main`. No head given, use current branch.

User may add free-text description of intended change, expected behavior, or review focus. Use it to interpret diff and judge whether implementation matches stated intent.

Treat as pull request, act as reviewer. Intent, scope, or success criteria still unclear after reading diff + description? Ask concise clarification questions before finishing.

Skip-tests trigger: `--skip-tests`, "skip tests", "no pytest", "don't run tests", or similar phrasing. When triggered, skip all pytest steps and section 3.

## Scope

- Diff branches locally at merge-base: `git diff <base>...<head>`. Read full diff plus surrounding code needed to understand it.
- **Only reflect on the changes**, not pre-existing code from before this branch.
- Pre-existing code forced the author's approach? **Note it, give slack** — nit at most, not a blocker.
- Write markdown report to `tmp/local-pr-review-{source_branch}({short-commit-id})_{target_branch}({short-commit-id}).md`.
- Unless skip-tests triggered, run pytest for touched areas (see **Pytest**), save to `tmp/local-pr-review-{source_branch}({short-commit-id})_{target_branch}({short-commit-id})-pytest.txt`.

## Output

Clean, readable Markdown. Section headings in the order below. Short paragraphs and bullets. Fenced code blocks only for commands or snippets. Consistent terminology and severity labels.

### 1. Intent & Summary (compact bullet list)

- **What** the branch does.
- **Why** problem it solves.
- **How** approach / key mechanisms, referencing relevant files and functions.
- One honest line on overall direction.

### 2. Findings (terse, one line per finding)

Caveman-review style: terse, actionable. One line each: location, problem, fix. No throat-clearing.

**Format:** `<file>:L<line>: <severity>: <problem>. <fix>.`

**Severity prefixes:**
- `🔴 bug:` — broken behavior, will cause an incident
- `🟡 risk:` — works but fragile (race, missing null check, swallowed error, magic number, latent trap)
- `🔵 nit:` — style, naming, micro-optim, dead code. Author can ignore
- `❓ q:` — genuine question, not a suggestion
- `✅ good:` — notably good change (sparingly)

**Rules:**
- Exact line numbers, exact symbol names in backticks.
- Concrete fix, not "consider refactoring".
- Include the *why* only when not obvious from the problem.
- No hedging ("perhaps", "maybe", "I think") — if unsure, use `q:`.
- Don't restate what the line does.
- Distinguish **active bugs** from **latent/hypothetical** issues. Safe today only via an unrelated code path? Say so, downgrade severity.
- Put the 3-5 highest-priority pre-merge checks first (crashes, data corruption, wrong results), each with file links.
- Note "slack given" inline in the relevant finding (usually `🔵 nit:`), no separate section.

**Auto-clarity exception:** For security findings (CVE-class), architectural disagreements, or a new author, write a normal paragraph with rationale, then resume terse.

### 3. Test Results (skip when skip-tests triggered)

- One-line summary: passed / failed / errored / skipped.
- Per failing/errored test: name, one-line error, classification (see **Pytest** for definitions).
- Link full output: `[pytest results](./local-pr-review-{source_branch}({short-commit-id})_{target_branch}({short-commit-id})-pytest.txt)`.

### 4. Architectural / Global notes (only when needed)

Cross-cutting observations or global constraints that don't fit a single finding. Concise bullets.

## Pytest

Run before writing the report, unless skip-tests triggered.

1. Identify touched Python modules from the diff. Files under `tests/` are the test targets, not source.
2. Map each changed module to its tests:
   - Test file under `tests/` mirroring the module path (`ml/models/foo.py` matches `tests/ml/models/test_foo.py`).
   - Any test file importing or referencing a changed symbol.
3. Run only those files:
   ```
   pytest <matched-test-files> -v --tb=short 2>&1 | tee tmp/local-pr-review-{source_branch}({short-commit-id})_{target_branch}({short-commit-id})-pytest.txt
   ```
4. No matching files found: note it in the report, skip the run.
5. Classify each failing test:
   - **Stale test** — asserts old behaviour the PR intentionally changed (hardcoded expected value, removed parameter, renamed symbol). Fix the test, not the code.
   - **Regression** — implementation broken or change introduced a regression.

## Boundaries

Review only. No code fix, no approve/request-changes, no linters. Output ready to paste into the PR.
