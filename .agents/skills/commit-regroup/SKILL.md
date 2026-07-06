---
name: commit-regroup
description: 'Analyze commits on a branch vs a target branch, cluster related commits by feature / bugfix / introduced concept, and emit a caveman-styled report suggesting how to interactive-rebase or cherry-pick each cluster into its own branch or PR. READ-ONLY: never edits code, never runs rebase/cherry-pick/reset — only inspects git and prints commands to run. Use when user says "group my commits", "which commits go together", "split this branch into PRs", "regroup commits", "cherry-pick plan", "organize commits for rebase", "clean up branch history".'
argument-hint: '[head-branch (default: current HEAD)] [target-branch (default: origin/main)]'
---

# Commit Regroup

Cluster branch commits by what they actually do, then tell user how to split them into rebasable / cherry-pickable units.

Report output uses **caveman style** (see [caveman skill](../caveman/SKILL.md)) — terse, fragments OK, drop articles/filler, all technical substance + exact commit hashes/branch names preserved verbatim.

## When to Use

- Branch grew messy, many commits, want to split into focused PRs.
- Want to know which commits belong together before interactive-rebase.
- Want a cherry-pick plan onto a fresh branch off target.

## Hard Constraints

- **READ-ONLY.** Allowed git: `status`, `fetch`, `log`, `show`, `diff`, `merge-base`, `rev-parse`, `branch`, `remote`, `cherry`, `diff-tree`. 
- **NEVER run** `rebase`, `cherry-pick`, `reset`, `commit`, `push`, `checkout -b`, `stash` (except when user explicitly approves stash for dirty-tree handling) or any code edit.
- Only *print* the rebase/cherry-pick commands. User runs them.

## Inputs & Defaults

| Input | Default |
|-------|---------|
| head branch | current `HEAD` (`git rev-parse --abbrev-ref HEAD`) |
| target branch | `origin/main` |

## Procedure

### 1. Resolve head + dirty check
1. `git rev-parse --abbrev-ref HEAD` → head branch (unless user gave one).
2. `git status --porcelain` → check uncommitted changes.
3. **If dirty**: STOP and ask user what to do. Offer:
   - analyze committed history only (ignore working tree),
   - user stashes/commits first then re-run,
   - user approves a `git stash` (only with explicit yes).
   Do not proceed on a dirty tree without an answer.

### 2. Resolve target + range
1. `git fetch <remote>` for the target's remote if reachable (read-only; skip if offline).
2. `git merge-base <target> <head>` → base.
3. `git log --no-merges --pretty=format:'%H%x09%s' <base>..<head>` → candidate commits (oldest→newest matters for rebase).

### 3. Gather per-commit facts
For each commit collect:
- short hash (`%h`), full subject.
- files touched: `git show --stat --oneline <hash>` or `git diff-tree --no-commit-id --name-only -r <hash>`.
- optional body/keywords: `git show -s --format=%b <hash>`.

### 3b. Detect already-in-target + conflict risk
Branch changes may already exist in target, or clash with target-side changes.

1. **Already applied (equivalent patch):** `git cherry <target> <head>` → lines starting `-` = commit already in target (patch-equivalent), lines `+` = not yet there. Mark `-` commits **ALREADY-IN-TARGET** → drop from cherry-pick/rebase plan.
2. **Same file changed on target since base:** `git diff --name-only <base>..<target>` → target-side touched files. Any branch commit touching those files = **CONFLICT-RISK** (target moved underneath it).
3. **Content overlap sanity check** (optional, for flagged files): `git diff <base>..<target> -- <file>` vs the commit's diff on same file → if same region touched, high conflict likelihood; if disjoint regions, low.
4. Empty/no-op after target merge: if a commit's diff is fully contained in target already but `git cherry` didn't catch it (e.g. squashed), flag **LIKELY-REDUNDANT** and tell user to verify with `git show <hash>` vs current target.

Use these flags in step 5 report. Do not silently include already-applied or redundant commits in the plan.

### 4. Cluster by subject
Group commits into **subjects** = one feature, one bugfix, or one introduced concept. Signals, in priority:
1. **Semantic intent** — same feature/fix/concept (primary; read subject+body).
2. **File/path overlap** — commits touching same module/dir reinforce a group.
3. **Commit-type prefix** — `feat:`/`fix:`/`refactor:` scope hints.

Rules:
- A commit belongs to exactly one subject. If it spans two, flag it as **mixed** → recommend splitting (`git rebase -i` + `edit` → `git reset -p`).
- Preserve chronological order inside each subject (rebase safety).
- Note cross-subject dependencies (subject B edits code subject A introduced) — order matters for cherry-pick.

#### Shared files across subjects
A single file can be touched by commits belonging to **different** subjects. File overlap alone does NOT force two subjects to merge — semantic intent wins. But it creates ordering/conflict coupling:

- **Same file, different regions/lines** (disjoint hunks): subjects stay separate. Note as **SHARED-FILE (disjoint)** — cherry-picking either first is usually clean. Compare hunk ranges via `git diff-tree -p <hash> -- <file>` to confirm disjoint.
- **Same file, same/overlapping lines**: subjects are **coupled**. Splitting them into independent PRs will conflict. Flag **SHARED-FILE (overlap)** → recommend either (a) keep coupled subjects in one PR, or (b) stack the PRs (later subject branches off earlier subject's branch), preserving chronological order.
- Record which subjects share each hot file so the PR-split topology (independent vs stacked) reflects it.

### 5. Emit caveman report

Format:

```
# COMMIT REGROUP — <head> vs <target>
base <shorthash>  |  N commits  |  M subjects  |  dirty: yes/no
already-in-target: K commits dropped  |  conflict-risk: J commits

## SUBJECT 1: <name> — feat|fix|refactor|concept
commits (order):
  <h1> <subject>
  <h2> <subject>  [CONFLICT-RISK: target moved path/a]
touch: path/a, path/b
shared: path/a also in SUBJECT 2 (overlap) → coupled
dep: none | needs SUBJECT k first
plan:
  cherry-pick: git switch -c <suggested-branch> <target> && git cherry-pick <h1> <h2>
  or rebase: git rebase -i <base>  # reorder → group these, `pick` them contiguous

## SUBJECT 2: <name> — feat|fix|refactor|concept
> depends on: [SUBJECT 1: <name>](#subject-1-name--featfixrefactorconcept)
commits (order):
  ...

## ALREADY IN TARGET (drop from plan)
  <hz> <subject> — patch-equivalent in <target> (git cherry `-`); verify: git show <hz>

## CONFLICT RISK vs TARGET
  <hx> touches path/a which target changed since base → expect conflict on cherry-pick/rebase

## MIXED / SPLIT NEEDED
  <hx> touches both <A> and <B> → git rebase -i <base>, mark `edit`, git reset -p, recommit halves

## SHARED FILES (cross-subject)
  path/a: SUBJECT 1 + SUBJECT 2, overlapping lines → keep in one PR or stack
  path/c: SUBJECT 1 + SUBJECT 3, disjoint lines → safe to split

## ORPHANS
  <hy> <subject> — standalone, own PR

## SUGGESTED PR SPLIT
  independent (no deps, no shared-overlap): PR1 = SUBJECT 1, PR2 = SUBJECT 2  (each branches off <target>)
  stacked (deps or shared-overlap): PR1 = SUBJECT A off <target>; PR2 = SUBJECT B off PR1 branch
```

Branch-name pattern: `<type>/<subject-slug>` (type = feat/fix/refactor; slug = kebab of subject). User may override.

PR topology:
- **No deps + no shared-overlap** between subjects → independent branches, each off `<target>`, independent PRs.
- **Deps exist** (B needs A) **or shared-overlap file** (B and A edit same lines) → stacked: branch A off `<target>`, branch B off A's branch; PR B targets PR A's branch.

Keep prose caveman. Hashes, branch names, commands verbatim and correct.

**Dependency callout rule:** Any subject that depends on another must open with a `> depends on:` blockquote listing markdown links to each prerequisite subject's header (using GitHub-style anchor: lowercase, spaces→hyphens, punctuation stripped). Example: `> depends on: [SUBJECT 1: my-feature](#subject-1-my-feature--feat)`. Place this immediately after the `## SUBJECT N:` heading line, before `commits (order):`.

### 6. Write report to file

1. Determine output filename: `commit-regroup-{branch_name}({start-short-commit-id}-{end-short-commit-id}).md`
   - `branch_name` = head branch name (slashes replaced with `_`)
   - `start-short-commit-id` = short hash of oldest commit in range (base-side)
   - `end-short-commit-id` = short hash of newest commit in range (HEAD-side)
2. Write the full report to `tmp/<filename>` in the workspace root.
3. Tell user: `report → tmp/<filename>`

### 7. Command correctness
- Cherry-pick plan: always `git switch -c <newbranch> <target>` then `git cherry-pick <hashes in chronological order>`.
- If subjects have deps, cherry-pick dependency subject first (or onto same branch in order).
- Interactive-rebase plan: `git rebase -i <base>`; tell user to reorder lines so each subject's `pick`s are contiguous; mention `--onto <target>` when moving whole subject off current base.
- Warn: cherry-pick makes new hashes; rebase rewrites history → don't rewrite pushed/shared branches without force + team awareness.

## Completion Check

- Every commit in `<base>..<head>` appears in exactly one of: a SUBJECT, ALREADY-IN-TARGET, CONFLICT-RISK, MIXED, or ORPHANS.
- Commits already in target (via `git cherry`) are flagged and excluded from the cherry-pick/rebase plan.
- Commits touching target-modified files are flagged CONFLICT-RISK.
- Cross-subject shared files are listed with same-line (overlap → couple/stack) vs different-line (disjoint → safe) distinction.
- Every subject has a concrete cherry-pick OR rebase command with real hashes.
- Dependency order stated where it matters.
- Every subject with deps opens with a `> depends on:` blockquote containing markdown anchor links to prerequisite subject headers.
- Report written to `tmp/commit-regroup-{branch_name}({start}-{end}).md` and path reported to user.
- No mutating git command was executed.
