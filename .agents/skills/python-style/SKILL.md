---
name: python-style
description: Use when writing Python — covers standard-library-first, pathlib, argparse, and type hints.
---

# Python Style

## Environment & dependencies

- **Standard library first:** prefer built-ins (`os`, `sys`, `json`) over
  third-party dependencies.
- **Path handling:** use `from pathlib import Path`, never string path
  manipulation.

## Interface

- **Argument parsing:** use `argparse` for robustness and auto-generated help.

## Type safety

- **Type hints:** annotate all function signatures (`list`, `Optional`, …) to
  make contracts explicit.
