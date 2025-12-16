#!/bin/bash

echo "🏡 Hall Collins Listing Packet Combiner - Installing Requirements"
echo "================================================================"
echo ""

# Check if we're on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "❌ This installer is designed for macOS. Please install manually:"
    echo "   pip3 install reportlab pillow PyPDF2"
    exit 1
fi

echo "� Current user: $(whoami)"
echo "📍 Current directory: $(pwd)"
echo ""

# Function to run command and check success
run_command() {
    echo "⚙️  Running: $1"
    if eval "$1"; then
        echo "✅ Success!"
        echo ""
        return 0
    else
        echo "❌ Failed: $1"
        echo ""
        return 1
    fi
}

# Check Python installation first
echo "🐍 Checking Python installation..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo "✅ Python found: $PYTHON_VERSION"
else
    echo "❌ Python3 not found. Installing via Homebrew..."
    if command -v brew &> /dev/null; then
        run_command "brew install python3"
    else
        echo "❌ Homebrew not found. Please install Python3 manually:"
        echo "   1. Visit https://python.org"
        echo "   2. Download Python 3.x for macOS"
        echo "   3. Install and try again"
        read -p "Press Enter to exit..."
        exit 1
    fi
fi

echo ""
echo "📦 Installing required Python libraries..."
echo ""

# Try multiple installation methods
INSTALL_SUCCESS=false

# Method 1: Standard pip3 install
echo "🔧 Method 1: Standard pip3 installation..."
if run_command "pip3 install --user reportlab pillow PyPDF2"; then
    INSTALL_SUCCESS=true
else
    echo "⚠️  Method 1 failed, trying alternative approaches..."
fi

# Method 2: Try without --user flag if Method 1 failed
if [ "$INSTALL_SUCCESS" = false ]; then
    echo "🔧 Method 2: System-wide installation..."
    if run_command "pip3 install reportlab pillow PyPDF2"; then
        INSTALL_SUCCESS=true
    fi
fi

# Method 3: Try with python -m pip if pip3 direct doesn't work
if [ "$INSTALL_SUCCESS" = false ]; then
    echo "🔧 Method 3: Using python -m pip..."
    if run_command "python3 -m pip install --user reportlab pillow PyPDF2"; then
        INSTALL_SUCCESS=true
    fi
fi

# Method 4: Try upgrading pip first, then installing
if [ "$INSTALL_SUCCESS" = false ]; then
    echo "🔧 Method 4: Upgrading pip and retrying..."
    run_command "python3 -m pip install --upgrade pip"
    if run_command "python3 -m pip install --user reportlab pillow PyPDF2"; then
        INSTALL_SUCCESS=true
    fi
fi

echo ""
echo "🧪 Testing installation..."
echo ""

# Comprehensive test of the installation
python3 << 'EOF'
import sys
import os

print(f"🐍 Python version: {sys.version}")
print(f"📁 Python executable: {sys.executable}")
print("")

missing_libs = []
success_libs = []

# Test ReportLab
try:
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.units import inch
    from reportlab.lib import colors
    
    # Test creating a simple PDF
    import tempfile
    test_path = tempfile.mktemp(suffix='.pdf')
    test_canvas = canvas.Canvas(test_path)
    test_canvas.drawString(100, 750, "Test PDF")
    test_canvas.save()
    os.unlink(test_path)
    
    success_libs.append("ReportLab")
    print('✅ ReportLab installed and working correctly')
except ImportError as e:
    missing_libs.append(f"ReportLab: {e}")
    print(f'❌ ReportLab failed: {e}')
except Exception as e:
    missing_libs.append(f"ReportLab (functionality): {e}")
    print(f'❌ ReportLab import OK but functionality failed: {e}')

# Test PIL/Pillow
try:
    from PIL import Image, ImageTk, ImageDraw, ImageFont
    
    # Test creating a simple image
    test_img = Image.new('RGB', (100, 100), 'white')
    
    success_libs.append("PIL/Pillow")
    print('✅ PIL/Pillow installed and working correctly')
except ImportError as e:
    missing_libs.append(f"PIL/Pillow: {e}")
    print(f'❌ PIL/Pillow failed: {e}')
except Exception as e:
    missing_libs.append(f"PIL/Pillow (functionality): {e}")
    print(f'❌ PIL/Pillow import OK but functionality failed: {e}')

# Test PyPDF2
try:
    from PyPDF2 import PdfMerger
    import PyPDF2
    
    success_libs.append("PyPDF2")
    print('✅ PyPDF2 installed and working correctly')
except ImportError as e:
    missing_libs.append(f"PyPDF2: {e}")
    print(f'❌ PyPDF2 failed: {e}')

print("")
print("📊 INSTALLATION SUMMARY:")
print("="*50)

if success_libs:
    print("✅ Successfully installed:")
    for lib in success_libs:
        print(f"   • {lib}")

if missing_libs:
    print("")
    print("❌ Failed to install:")
    for lib in missing_libs:
        print(f"   • {lib}")
    print("")
    print("🔧 TROUBLESHOOTING STEPS:")
    print("1. Close this window")
    print("2. Open Terminal (Applications > Utilities > Terminal)")
    print("3. Run these commands one by one:")
    print("   python3 -m pip install --upgrade pip")
    print("   python3 -m pip install --user reportlab")
    print("   python3 -m pip install --user pillow")
    print("   python3 -m pip install --user PyPDF2")
    print("4. After each command, check if it says 'Successfully installed'")
    sys.exit(1)
else:
    print("")
    print("🎉 ALL LIBRARIES INSTALLED SUCCESSFULLY!")
    print("")
    print("✅ Your Hall Collins Listing Packet Combiner is ready!")
    print("🚀 You can now double-click 'Hall Collins Listing Packet Combiner.command'")
    print("🎯 All features including cover pages and Instagram posts will work!")

EOF

if [ $? -eq 0 ]; then
    echo ""
    echo "🎊 INSTALLATION COMPLETE!"
    echo ""
    echo "✅ All required libraries are installed and working"
    echo "🚀 You can now run the Hall Collins Listing Packet Combiner"
    echo ""
else
    echo ""
    echo "❌ INSTALLATION INCOMPLETE"
    echo ""
    echo "Some libraries failed to install. Please:"
    echo "1. Take a screenshot of any error messages above"
    echo "2. Contact technical support"
    echo "3. Or try manual installation in Terminal"
fi

echo ""
read -p "Press Enter to close this window..."
