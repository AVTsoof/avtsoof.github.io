#!/usr/bin/env bash

# Setup script for MkDocs Portfolio environment
# Installs dependencies listed in requirements.txt

if ! command -v pip &> /dev/null; then
    echo "pip is not installed. Please install Python and pip."
    exit 1
fi

echo "Installing project dependencies..."
pip install -r requirements.txt --user

echo "Dependencies installed successfully."
