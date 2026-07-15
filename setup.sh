#!/usr/bin/env bash
set -euo pipefail

# Setup script for the MkDocs blog environment.

if ! command -v python3 &> /dev/null; then
    echo "python3 is not installed. Please install Python 3." >&2
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d .venv ]; then
    echo "Creating virtual environment (.venv)..."
    python3 -m venv .venv
fi

# Install dependencies (includes the editable toolkit via `-e .` in requirements.txt)
echo "Installing dependencies from requirements.txt..."
./.venv/bin/python -m pip install -r requirements.txt

# Activate the versioned git hooks (pre-push strict-build gate) - once per clone
echo "Configuring git hooks (core.hooksPath -> .githooks)..."
git config core.hooksPath .githooks

echo "Setup complete!"
echo "To run the server, execute: ./.venv/bin/mkdocs serve"
