#!/bin/bash

echo "🚀 SUPER SIMPLE Library Installer for Hall Collins App"
echo "====================================================="
echo ""
echo "This will install the required libraries using EVERY possible method"
echo ""

# Function to test if a library is working
test_library() {
    python3 -c "
try:
    $2
    print('✅ $1 is working')
    exit(0)
except:
    print('❌ $1 is NOT working')
    exit(1)
" 2>/dev/null
    return $?
}

# Test what's already working
echo "🧪 Testing current library status..."
test_library "ReportLab" "from reportlab.pdfgen import canvas"
REPORTLAB_OK=$?

test_library "PIL/Pillow" "from PIL import Image, ImageTk"
PIL_OK=$?

test_library "PyPDF2" "from PyPDF2 import PdfMerger"
PYPDF2_OK=$?

if [ $REPORTLAB_OK -eq 0 ] && [ $PIL_OK -eq 0 ] && [ $PYPDF2_OK -eq 0 ]; then
    echo ""
    echo "🎉 All libraries are already working!"
    echo "✅ Your app should work perfectly"
    read -p "Press Enter to close..."
    exit 0
fi

echo ""
echo "📦 Installing missing libraries..."
echo ""

# Array of installation commands to try
declare -a commands=(
    "pip3 install --user reportlab pillow PyPDF2"
    "pip3 install reportlab pillow PyPDF2"
    "python3 -m pip install --user reportlab pillow PyPDF2"
    "python3 -m pip install reportlab pillow PyPDF2"
    "/usr/local/bin/pip3 install --user reportlab pillow PyPDF2"
    "python3 -m pip install --user --upgrade pip && python3 -m pip install --user reportlab pillow PyPDF2"
)

# Try each installation command
for cmd in "${commands[@]}"; do
    echo "🔧 Trying: $cmd"
    if eval "$cmd"; then
        echo "✅ Installation command succeeded"
        
        # Test if it actually worked
        sleep 2
        test_library "ReportLab" "from reportlab.pdfgen import canvas"
        REPORTLAB_OK=$?
        
        test_library "PIL/Pillow" "from PIL import Image, ImageTk"
        PIL_OK=$?
        
        test_library "PyPDF2" "from PyPDF2 import PdfMerger"
        PYPDF2_OK=$?
        
        if [ $REPORTLAB_OK -eq 0 ] && [ $PIL_OK -eq 0 ] && [ $PYPDF2_OK -eq 0 ]; then
            echo ""
            echo "🎊 SUCCESS! All libraries are now working!"
            break
        else
            echo "⚠️  Installation completed but libraries still not working, trying next method..."
        fi
    else
        echo "❌ Installation command failed, trying next method..."
    fi
    echo ""
done

echo ""
echo "🧪 Final test..."

# Final comprehensive test
python3 -c "
import sys

print('🔍 Final library verification:')
print('')

success = True

try:
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter
    import tempfile
    import os
    
    # Test creating a PDF
    test_path = tempfile.mktemp(suffix='.pdf')
    c = canvas.Canvas(test_path)
    c.drawString(100, 750, 'Test')
    c.save()
    os.unlink(test_path)
    
    print('✅ ReportLab: WORKING (can create PDFs)')
except Exception as e:
    print(f'❌ ReportLab: FAILED - {e}')
    success = False

try:
    from PIL import Image, ImageTk, ImageDraw
    
    # Test creating an image
    img = Image.new('RGB', (100, 100), 'white')
    draw = ImageDraw.Draw(img)
    draw.text((10, 10), 'Test', fill='black')
    
    print('✅ PIL/Pillow: WORKING (can create images)')
except Exception as e:
    print(f'❌ PIL/Pillow: FAILED - {e}')
    success = False

try:
    from PyPDF2 import PdfMerger
    merger = PdfMerger()
    print('✅ PyPDF2: WORKING (can merge PDFs)')
except Exception as e:
    print(f'❌ PyPDF2: FAILED - {e}')
    success = False

print('')

if success:
    print('🎉 ALL LIBRARIES WORKING PERFECTLY!')
    print('🚀 Your Hall Collins app will now show the full GUI!')
    print('')
    print('✅ You can now run: Hall Collins Listing Packet Combiner.command')
else:
    print('❌ Some libraries are still not working.')
    print('')
    print('🔧 MANUAL INSTALLATION REQUIRED:')
    print('1. Open Terminal (Applications > Utilities > Terminal)')
    print('2. Copy and paste each line below, pressing Enter after each:')
    print('')
    print('   python3 -m pip install --upgrade pip')
    print('   python3 -m pip install --user reportlab')
    print('   python3 -m pip install --user pillow')  
    print('   python3 -m pip install --user PyPDF2')
    print('')
    print('3. After each command, look for \"Successfully installed\"')
    print('')
    print('💡 If you still have issues, Python may need to be reinstalled')
    print('   Download from: https://www.python.org/downloads/')

"

echo ""
read -p "Press Enter to close this window..."
