#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
VENV_DIR = ROOT / ".venv"


def venv_python() -> Path:
    """Return the path to the Python executable inside the virtual environment."""
    if sys.platform == "win32":
        return VENV_DIR / "Scripts" / "python.exe"
    return VENV_DIR / "bin" / "python"


def should_recreate(override: bool) -> bool:
    """Decide whether to recreate an existing virtual environment."""
    if not VENV_DIR.exists():
        return False
    if override:
        print("--override specified: recreating the existing virtual environment (.venv)...")
        return True
    print("A virtual environment (.venv) already exists.")
    answer = input(
        "Override it (delete and recreate) or install on top? "
        "[o]verride / [i]nstall (default: install): "
    ).strip().lower()
    if answer in ("o", "override"):
        return True
    print("Installing requirements on top of the existing virtual environment...")
    return False


def main() -> int:
    parser = argparse.ArgumentParser(description="Set up the MkDocs blog environment.")
    parser.add_argument(
        "--override",
        action="store_true",
        help="Recreate the virtual environment from scratch without prompting.",
    )
    args = parser.parse_args()

    if should_recreate(args.override):
        print("Removing existing virtual environment (.venv)...")
        shutil.rmtree(VENV_DIR)

    if not VENV_DIR.exists():
        print("Creating virtual environment (.venv)...")
        subprocess.run([sys.executable, "-m", "venv", str(VENV_DIR)], check=True)

    print("Installing dependencies from requirements.txt...")
    subprocess.run(
        [str(venv_python()), "-m", "pip", "install", "-r", "requirements.txt"],
        check=True,
        cwd=ROOT,
    )

    print("Configuring git hooks (core.hooksPath -> .githooks)...")
    subprocess.run(["git", "config", "core.hooksPath", ".githooks"], check=True, cwd=ROOT)

    print("Setup complete!")
    mkdocs = "mkdocs" if sys.platform != "win32" else "mkdocs.exe"
    print(f"To run the server, execute: {venv_python().parent / mkdocs} serve")
    return 0


if __name__ == "__main__":
    sys.exit(main())
