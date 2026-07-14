---
name: pr-orchestrator
description: Use this skill to generate concise, reviewer-focused pull request descriptions that explain what changed, why it changed, how to review it, and what areas require extra attention.
argument-hint: '<headBranch> [baseBranch=main]'
allowed-tools: [shell, git, markdown]
---

# Instructions

You are an expert code review assistant. When this skill is active, analyze the pull request diff, commit messages, and changed files, then generate a reviewer-oriented PR description.

Use the branch names provided as arguments. If no head branch is given, use the current branch. If the base branch is omitted, assume `main`.

This skill only *describes* the change to peers (what / why / how / what to look at). It does **not** review the code, judge quality, or assign severity — it is an authoring tool, not a reviewer.

Default structural style for this workspace:
- Use a compact `## What` table with three columns: `What | Why | How`.
- Keep `## Changes` as the primary reviewer-order section.
- Add `## Example usage` when behavior/config/workflow changes are introduced.
- Treat `Watch areas`, `Breaking changes`, `Migration steps`, `Dependencies changes`, and `Testing` as optional sections; include only when requested or when materially needed.
- Wrap file references and code objects in backticks in markdown output.

Follow this workflow:

1. Gather context about the changes (base defaults to `main`):
   ```bash
   git diff <base>...<head>
   git log --oneline <base>..<head>
   ```
   Use the merge-base diff (`...`) to understand the code changes and the commit history to understand the intent behind them. Read the surrounding code you need to understand *why* a change was made, not just the diff lines.

2. Identify the main purpose of the PR.

3. Group related file changes into logical change sets rather than listing files individually.

4. Summarize the reason behind the changes and their expected impact.

5. Suggest a review order that helps reviewers understand dependencies and context efficiently.

6. Optionally highlight high-risk/complex/performance-sensitive areas when they add reviewer value.

7. Optionally mention breaking changes, migration requirements, configuration changes, or backward compatibility concerns.

8. Exclude trivial implementation details unless they are important for understanding the behavior change.

9. Focus on helping reviewers review the PR quickly and accurately.

10. Add practical usage snippets when new capabilities are introduced (callbacks, config presets, CLI flows, logger setup).

Generate output using the following template:

```markdown
# <PR_TITLE>

## What
| What | Why | How |
| --- | --- | --- |
| [Change summary] | [Motivation/value] | [Implementation summary with key symbol(s)] |

## Changes

List logical changes in review priority order (highest-impact / dependency-first first).

1. [Logical change area]
   - path/to/file.py:Lx-Ly `symbol_name` — reason this should be reviewed first
2. [Logical change area]
   - path/to/file.py:Lx-Ly `symbol_name` — key behavior change
3. [Logical change area]
   - path/to/file.py:Lx-Ly `symbol_name` — integration or validation logic

## Example usage
- [Scenario]

```yaml
# Minimal config snippet for the new behavior
```

- [Scenario]

```bash
# Minimal CLI invocation
```

## Watch areas
- [Complex logic or edge case reviewers should look at closely]
- [Compatibility concern]
- [Area most likely to need extra attention]

## Breaking changes (if any)
- [Description of breaking change]

## Migration steps (if any)
- [Migration step description]

## Dependencies changes (if any)
- [Dependency name] — reason for the change or update

## Testing
- Automated tests
- Manual validation

```

Section inclusion policy:
- Always include: `What` (table), `Changes`.
- Include `Example usage` when the PR adds/changes runtime behavior, callback wiring, config contracts, or CLI workflow.
- Omit any empty optional section.
- If the user asks for a shorter doc, keep only `What`, `Changes`, and (if useful) `Example usage`.

Formatting and output guidelines:

- Use the section headings above, in the same order.
- Use short paragraphs and bullet lists for scanability; avoid dense text blocks.
- Use fenced code blocks only for commands or snippets.
- Order the `Changes` list by priority: the highest-impact / dependency-first changes come first.
- Prefer grouping changes by feature, behavior, or subsystem.
- Explain intent before implementation details.
- Optimize for reducing reviewer cognitive load.
- Use `git diff <base>...<head>` as the primary source of truth for code changes.
- Use `git log --oneline <base>..<head>` to infer intent and feature boundaries.
- Avoid producing a file-by-file changelog unless explicitly requested.
- In markdown output, wrap file references and code symbols in backticks.

References and length (target is the Azure DevOps PR description textbox):

- Reference changes with **plain text only**: file name, line numbers (`path/to/file.py:Lx-Ly`), and the names of key symbols/references in backticks. Do **not** use markdown links or URLs — they waste characters and do not render in the Azure DevOps textbox.
- Keep the description compact so it fits the Azure DevOps PR description limit. Aim for ~300 words and do not exceed ~500 words. Omit any section that has no content.
- Write the PR description into a markdown file named `tmp/pr-description-{source_branch}({short-commit-id})_{target_branch}({short-commit-id}).md`.
