---
name: clean-code
description: Use when writing or reviewing code in any language — covers naming, comments, SRP, guard clauses, pure functions, and fail-fast robustness.
---

# Clean Code (language-agnostic)

## Naming & comments

- **Self-documenting code:** names should be descriptive enough that comments are
  unnecessary.
- **Comment the *why*:** explain intent or business logic, never the syntax.
- **No magic literals:** replace raw strings/numbers with named constants or
  enums (`MAX_RETRY_COUNT`, not `3`).

## Function architecture

- **Single Responsibility (SRP):** a function does one thing; if its description
  needs "and", split it.
- **Guard clauses:** return early instead of deeply nested `if/else`.
- **Pure functions:** avoid side effects where possible — output depends only on
  input.

## Robustness & safety

- **Fail fast:** validate inputs at the top of a function; crash early rather than
  process corrupted data.
- **Logging over printing:** use a logging framework with levels, not stdout, for
  application logs.
- **Deterministic output:** sort inputs/outputs (by id/timestamp) for consistent
  checksums and easy diffing.

## Interface flexibility

- **Hybrid execution:** tools should support both a single explicit target and
  auto-scanning batch mode depending on arguments.
