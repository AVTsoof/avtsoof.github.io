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

# Install dependencies
Write-Host "Installing dependencies from requirements.txt..."
.\.venv\Scripts\python -m pip install -r requirements.txt

Write-Host "Setup complete!"
Write-Host "To run the server, execute: .\.venv\Scripts\mkdocs serve"
