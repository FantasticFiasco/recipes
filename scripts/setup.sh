#!/bin/bash
# Quick Start Script for Recipe Importer
#
# This script sets up a virtual environment and installs dependencies

set -e

echo "Setting up Recipe Importer..."
echo ""

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is required but not found."
    echo "Please install Python 3.8 or higher."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip > /dev/null 2>&1
pip install -r requirements.txt

echo ""
echo "✓ Setup complete!"
echo ""
echo "Usage:"
echo "  source venv/bin/activate                    # Activate environment"
echo "  python import_recipes.py <url>              # Import single recipe"
echo "  python import_recipes.py --file urls.txt    # Import multiple recipes"
echo "  deactivate                                  # Deactivate environment when done"
echo ""
