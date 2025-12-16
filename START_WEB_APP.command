#!/bin/bash

# Hall Collins Listing Packet Combiner - Web App Launcher
# This script starts the web version of the application

echo "🌐 Hall Collins Listing Packet Combiner - Web Version"
echo "=================================================="
echo ""

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "$SCRIPT_DIR"

# Check if the web app file exists
if [ ! -f "web_app.py" ]; then
    echo "❌ ERROR: web_app.py not found!"
    echo "Make sure this script is in the same folder as the web app file."
    read -p "Press Enter to close..."
    exit 1
fi

# Check if Streamlit is installed
echo "🔍 Checking Streamlit installation..."
if ! command -v streamlit &> /dev/null; then
    echo "❌ Streamlit not found. Installing web dependencies..."
    echo ""
    
    if command -v pip3 &> /dev/null; then
        pip3 install -r requirements-web.txt
    elif command -v pip &> /dev/null; then
        pip install -r requirements-web.txt
    else
        echo "❌ ERROR: pip not found. Please install Python first."
        echo ""
        echo "Solutions:"
        echo "1. Install Python 3 from https://python.org"
        echo "2. Run 'SETUP - Run This First.command'"
        echo ""
        read -p "Press Enter to close..."
        exit 1
    fi
fi

# Start the web application
echo ""
echo "🚀 Starting Hall Collins Web Application..."
echo ""
echo "📱 The app will open in your web browser at:"
echo "   http://localhost:8501"
echo ""
echo "🔗 Share this link with agents for access:"
echo "   http://your-computer-ip:8501"
echo ""
echo "⏹️  To stop the server: Press Ctrl+C in this window"
echo ""

# Launch Streamlit
streamlit run web_app.py

echo ""
echo "📱 Web application stopped."
read -p "Press Enter to close this window..."
