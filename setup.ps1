# Setup script for MkDocs Portfolio environment on Windows
Write-Host "Checking Python installation..."
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Error "Python is not installed or not in PATH. Please install Python."
    exit
}

# Create virtual environment if it doesn't exist
if (-not (Test-Path .venv)) {
    Write-Host "Creating virtual environment (.venv)..."
    python -m venv .venv
}

# Install dependencies (includes the editable toolkit via `-e .` in requirements.txt)
Write-Host "Installing dependencies from requirements.txt..."
.\.venv\Scripts\python -m pip install -r requirements.txt

# Activate the versioned git hooks (pre-push strict-build gate) - once per clone
Write-Host "Configuring git hooks (core.hooksPath -> .githooks)..."
git config core.hooksPath .githooks

Write-Host "Setup complete!"
Write-Host "To run the server, execute: .\.venv\Scripts\mkdocs serve"
