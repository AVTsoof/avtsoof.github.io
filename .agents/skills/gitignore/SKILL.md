---
name: gitignore
description: Use when editing `.gitignore` or deciding what to track — covers baseline templates, artifact-vs-source scope, secrets, and syntax pitfalls.
---

# .gitignore

## Baseline

- Don't reinvent the wheel: start from an industry-standard template
  (e.g. gitignore.io).
- Concatenate standard templates when combining technologies.

## Scope & hierarchy

- **Artifacts over source:** ignore anything a build command can recreate
  (`bin/`, `dist/`, `node_modules/`, `site/`).
- **Pragmatic pollution control:** add OS files (`.DS_Store`) and IDE folders
  (`.vscode/`, `.idea/`) even if they belong in a global config.

## Security & configuration

- **Secrets zero tolerance:** ignore local config holding secrets (`.env`).
- **Template pattern:** if ignoring `config.local.json`, commit a sanitized
  `config.example.json`.

## Syntax & maintenance

- **Whitelisting:** track an otherwise-ignored file with `!` *after* the ignore
  rule (e.g. `!vendor/lib/special.dll`).
- **The "cached" trap:** adding an already-committed file to `.gitignore` does
  nothing — run `git rm --cached <file>` to stop tracking while keeping it on
  disk.
