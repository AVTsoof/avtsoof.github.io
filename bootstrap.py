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


def available_projects() -> list[str]:
    """Return sorted names of existing sub-project directories under projects/."""
    projects_dir = ROOT / "projects"
    if not projects_dir.exists():
        return []
    return sorted(p.name for p in projects_dir.iterdir() if p.is_dir())


def install_project(slug: str) -> int:
    """Install a sub-project's requirements into the existing root venv."""
    if not VENV_DIR.exists():
        print("Error: root .venv not found. Run bootstrap.py first.", file=sys.stderr)
        return 1
    req = ROOT / "projects" / slug / "requirements.txt"
    if not req.exists():
        print(f"Error: {req} not found.", file=sys.stderr)
        return 1
    print(f"Installing {req} into root .venv...")
    subprocess.run(
        [str(venv_python()), "-m", "pip", "install", "-r", str(req)],
        check=True,
        cwd=ROOT,
    )
    print("Done.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Set up the MkDocs blog environment.")
    parser.add_argument(
        "--override",
        action="store_true",
        help="Recreate the virtual environment from scratch without prompting.",
    )
    projects = available_projects()
    parser.add_argument(
        "--project",
        metavar="SLUG",
        choices=projects or None,
        help=(
            f"Install a sub-project's requirements into the existing root .venv. "
            f"Available: [{', '.join(projects)}]"
            if projects
            else "Install a sub-project's requirements into the existing root .venv."
        ),
    )
    args = parser.parse_args()

    if args.project:
        return install_project(args.project)

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
