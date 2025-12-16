#!/bin/bash

# Hall Collins Listing Packet Combiner Launcher
# This script runs the Python application

echo "=========================================="
echo "Hall Collins Listing Packet Combiner"
echo "=========================================="
echo ""

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
echo "Working directory: $SCRIPT_DIR"

# Change to the script directory
cd "$SCRIPT_DIR"

# Check if the Python file exists
if [ ! -f "ultra_simple_combiner.py" ]; then
    echo "ERROR: ultra_simple_combiner.py not found!"
    echo "Make sure this script is in the same folder as the Python file."
    read -p "Press Enter to close..."
    exit 1
fi

# Check if Python 3 is available and run the application
echo ""
echo "Checking Python installation..."

if command -v python3 &> /dev/null; then
    echo "Found Python 3. Starting application..."
    echo ""
    python3 ultra_simple_combiner.py
elif command -v python &> /dev/null; then
    echo "Found Python. Starting application..."
    echo ""
    python ultra_simple_combiner.py
else
    echo ""
    echo "ERROR: Python is not installed or not found in PATH."
    echo ""
    echo "Solutions:"
    echo "1. Run 'SETUP - Run This First.command' to install Python dependencies"
    echo "2. Install Python 3 from https://python.org"
    echo "3. Make sure Python is in your system PATH"
    echo ""
    read -p "Press Enter to close..."
    exit 1
fi

echo ""
echo "Application closed."
read -p "Press Enter to close this window..."
