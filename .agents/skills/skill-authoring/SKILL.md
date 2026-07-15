---
name: skill-authoring
description: Use when creating or editing a skill under `.agents/skills/` — enforces minimalism and defines when to split a skill.
---

# Skill Authoring

## Minimalism

- Every skill stays as thin and low-token as possible: it points to the *one*
  right way to do a task, not an exhaustive manual.
- Prefer a short imperative checklist over prose. Link to code/examples instead
  of duplicating them.

## Structure

- Each skill is `.agents/skills/<name>/SKILL.md` with YAML front matter:
  ```yaml
  ---
  name: <name>
  description: Use when <trigger> — <one-line scope>.
  ---
  ```
- The `description` must state *when* to use the skill so it is discoverable.
- Co-locate a skill's helper scripts under `.agents/skills/<name>/scripts/`.

## When to split

- Split a skill only when it genuinely grows too large or covers two distinct
  triggers. Do not pre-emptively fragment; a single focused skill is preferred
  over several near-empty ones.
