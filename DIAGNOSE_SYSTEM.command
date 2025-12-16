#!/bin/bash

echo "🔍 Hall Collins Listing Packet Combiner - System Diagnostic"
echo "=========================================================="
echo ""
echo "📋 This diagnostic will help identify why the GUI isn't working"
echo ""

echo "💻 SYSTEM INFORMATION:"
echo "----------------------"
echo "🍎 macOS Version: $(sw_vers -productVersion)"
echo "👤 Current User: $(whoami)"
echo "📁 Current Directory: $(pwd)"
echo "🏠 Home Directory: $HOME"
echo ""

echo "🐍 PYTHON INFORMATION:"
echo "----------------------"
if command -v python3 &> /dev/null; then
    echo "✅ Python3 found: $(which python3)"
    echo "📦 Python version: $(python3 --version)"
    echo "📍 Python executable: $(python3 -c 'import sys; print(sys.executable)')"
    echo "📚 Python path:"
    python3 -c "import sys; [print(f'   • {p}') for p in sys.path if p]"
else
    echo "❌ Python3 NOT found"
    echo "💡 This is likely the problem - Python3 needs to be installed"
fi

echo ""
echo "📦 PIP INFORMATION:"
echo "-------------------"
if command -v pip3 &> /dev/null; then
    echo "✅ pip3 found: $(which pip3)"
    echo "📦 pip3 version: $(pip3 --version)"
else
    echo "❌ pip3 NOT found"
fi

echo ""
echo "📚 LIBRARY TESTING:"
echo "-------------------"

# Comprehensive library testing
python3 << 'EOF'
import sys
import os

def test_library(lib_name, import_func):
    try:
        import_func()
        print(f"✅ {lib_name}: WORKING")
        return True
    except ImportError as e:
        print(f"❌ {lib_name}: MISSING - {e}")
        return False
    except Exception as e:
        print(f"⚠️  {lib_name}: INSTALLED but BROKEN - {e}")
        return False

print("Testing required libraries...")
print("")

# Test tkinter (should be built-in)
tkinter_works = test_library("tkinter (GUI framework)", lambda: __import__('tkinter'))

# Test PyPDF2
pypdf2_works = test_library("PyPDF2 (PDF handling)", lambda: __import__('PyPDF2'))

# Test ReportLab
def test_reportlab():
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.units import inch
    from reportlab.lib import colors

reportlab_works = test_library("ReportLab (PDF creation)", test_reportlab)

# Test PIL/Pillow
def test_pil():
    from PIL import Image, ImageTk, ImageDraw, ImageFont

pil_works = test_library("PIL/Pillow (image handling)", test_pil)

print("")
print("📊 SUMMARY:")
print("="*40)

basic_features = tkinter_works and pypdf2_works
advanced_features = reportlab_works and pil_works

if basic_features:
    print("✅ Basic PDF combining: AVAILABLE")
else:
    print("❌ Basic PDF combining: NOT AVAILABLE")
    
if advanced_features:
    print("✅ Cover page & Instagram posts: AVAILABLE")
else:
    print("❌ Cover page & Instagram posts: NOT AVAILABLE")

print("")

if not tkinter_works:
    print("🚨 CRITICAL: tkinter missing - this means Python installation is incomplete")
    print("💡 SOLUTION: Reinstall Python from https://python.org")
    
elif not pypdf2_works:
    print("⚠️  ISSUE: PyPDF2 missing - basic PDF combining won't work")
    print("💡 SOLUTION: Run 'pip3 install PyPDF2'")
    
elif not (reportlab_works and pil_works):
    print("⚠️  ISSUE: Advanced libraries missing - only basic PDF combining available")
    print("💡 SOLUTION: Run the INSTALL_REQUIREMENTS.command script")
    
else:
    print("🎉 ALL LIBRARIES WORKING! The GUI should display properly.")
    print("")
    print("🤔 If the GUI still doesn't show, the issue might be:")
    print("   • Application permissions")
    print("   • File corruption") 
    print("   • Dropbox sync issues")

EOF

echo ""
echo "📱 FILE SYSTEM CHECK:"
echo "---------------------"
echo "📁 App files in current directory:"
if [ -f "ultra_simple_combiner.py" ]; then
    echo "✅ ultra_simple_combiner.py found"
    echo "📏 Size: $(ls -lh ultra_simple_combiner.py | awk '{print $5}')"
else
    echo "❌ ultra_simple_combiner.py NOT found"
fi

if [ -f "Hall Collins Listing Packet Combiner.command" ]; then
    echo "✅ Hall Collins Listing Packet Combiner.command found"
    echo "🔐 Permissions: $(ls -l 'Hall Collins Listing Packet Combiner.command' | awk '{print $1}')"
else
    echo "❌ Hall Collins Listing Packet Combiner.command NOT found"
fi

if [ -d "templates" ]; then
    echo "✅ templates folder found"
    echo "📂 Contains $(ls templates/ | wc -l) files"
else
    echo "❌ templates folder NOT found"
fi

echo ""
echo "🎯 NEXT STEPS:"
echo "-------------"
echo "1. Review the library test results above"
echo "2. If any libraries are missing, run: INSTALL_REQUIREMENTS.command"
echo "3. If Python3 is missing, install it from https://python.org"
echo "4. If everything shows as working, try running the test app:"
echo "   python3 test_missing_libraries.py"
echo ""
echo "📞 For support, take a screenshot of this diagnostic and contact IT"

echo ""
read -p "Press Enter to close this window..."
