#!/bin/bash

echo "🏡 Hall Collins Listing Packet Combiner - Complete Setup"
echo "========================================================"
echo ""
echo "This will help you get the Hall Collins app working on your computer."
echo ""

# Check if we're in the right place
if [ -f "ultra_simple_combiner.py" ] && [ -d "templates" ]; then
    echo "✅ You're already in the correct app folder!"
    echo "📁 Location: $(pwd)"
    echo ""
    echo "🧪 Testing the app files..."
    
    # Test Python
    if command -v python3 &> /dev/null; then
        echo "✅ Python3 found"
    else
        echo "❌ Python3 missing - need to install Python"
        echo "💡 Download from: https://python.org"
        read -p "Press Enter to continue anyway..."
    fi
    
    # Test app file
    if [ -f "ultra_simple_combiner.py" ]; then
        size=$(ls -lh "ultra_simple_combiner.py" | awk '{print $5}')
        echo "✅ Main app file found (Size: $size)"
        
        if [ "$size" = "0B" ]; then
            echo "❌ App file is empty - Dropbox sync issue"
            echo "💡 Try downloading the folder again from Dropbox web"
        fi
    fi
    
    # Test templates
    if [ -d "templates" ]; then
        template_count=$(ls templates/ | wc -l)
        echo "✅ Templates folder found ($template_count files)"
        
        if [ "$template_count" -eq 0 ]; then
            echo "❌ Templates folder is empty - Dropbox sync issue"
        fi
    fi
    
    echo ""
    echo "� NEXT STEPS:"
    echo "1. Run: SUPER_INSTALL.command (to install libraries)"
    echo "2. Run: Hall Collins Listing Packet Combiner.command (to start app)"
    
else
    echo "❌ App files not found in current location"
    echo "📁 Current location: $(pwd)"
    echo ""
    echo "🔍 Let's find the correct location..."
    
    # Search common locations
    locations=(
        "$HOME/Dropbox/Hall Collins REG Team Folder/Code/ListingPacketCombiner"
        "$HOME/Hall Collins REG Dropbox/Hall Collins REG Team Folder/Code/ListingPacketCombiner"
        "$HOME/Dropbox (Personal)/Hall Collins REG Team Folder/Code/ListingPacketCombiner"
        "$HOME/Desktop/ListingPacketCombiner"
        "$HOME/Downloads/ListingPacketCombiner"
    )
    
    found=false
    for location in "${locations[@]}"; do
        if [ -f "$location/ultra_simple_combiner.py" ]; then
            echo "✅ FOUND APP AT: $location"
            echo ""
            echo "🎯 SOLUTION:"
            echo "1. Open Finder"
            echo "2. Navigate to: $location" 
            echo "3. Double-click this file there: SETUP - Run This First.command"
            echo "4. Or run these files in order:"
            echo "   • SUPER_INSTALL.command"
            echo "   • Hall Collins Listing Packet Combiner.command"
            found=true
            break
        fi
    done
    
    if [ "$found" = false ]; then
        echo "❌ App not found in common locations"
        echo ""
        echo "� MANUAL DOWNLOAD STEPS:"
        echo ""
        echo "1. 🌐 Open web browser"
        echo "2. 📱 Go to dropbox.com and sign in"
        echo "3. 📁 Navigate to: Hall Collins REG Team Folder → Code"
        echo "4. 📦 Find 'ListingPacketCombiner' folder"
        echo "5. ⬇️  Click download (may download as ZIP)"
        echo "6. 📂 If ZIP, double-click to extract"
        echo "7. 🖥️  Move folder to Desktop"
        echo "8. 🔄 Run this setup script from inside that folder"
        echo ""
        echo "💡 Alternative: Ask someone to share the folder directly"
    fi
fi

echo ""
echo "🆘 IF YOU NEED HELP:"
echo "   📸 Take screenshot of this window"
echo "   📞 Contact IT support"
echo "   📧 Include your computer model and macOS version"

echo ""
read -p "Press Enter to close this window..."
