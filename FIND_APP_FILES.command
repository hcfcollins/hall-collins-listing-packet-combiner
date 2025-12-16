#!/bin/bash

echo "🔍 Hall Collins App - File Location Finder"
echo "=========================================="
echo ""

# Function to check if a path exists and show details
check_path() {
    local path="$1"
    local name="$2"
    
    if [ -e "$path" ]; then
        if [ -f "$path" ]; then
            size=$(ls -lh "$path" | awk '{print $5}')
            echo "✅ $name: FOUND at $path (Size: $size)"
        elif [ -d "$path" ]; then
            count=$(ls -1 "$path" | wc -l)
            echo "✅ $name: FOUND at $path ($count items)"
        fi
        return 0
    else
        echo "❌ $name: NOT FOUND at $path"
        return 1
    fi
}

echo "🔍 SEARCHING FOR HALL COLLINS APP FILES..."
echo ""

# Get current directory
current_dir=$(pwd)
echo "📁 Currently searching in: $current_dir"
echo ""

# Search for files in current directory
echo "📋 Checking current directory:"
check_path "./ultra_simple_combiner.py" "Main App File"
check_path "./Hall Collins Listing Packet Combiner.command" "App Launcher"
check_path "./templates" "Templates Folder"
check_path "./DIAGNOSE_SYSTEM.command" "Diagnostic Script"
check_path "./SUPER_INSTALL.command" "Super Installer"

echo ""
echo "🔍 SEARCHING COMMON LOCATIONS..."
echo ""

# Common Dropbox locations
dropbox_paths=(
    "$HOME/Dropbox/Hall Collins REG Team Folder/Code/ListingPacketCombiner"
    "$HOME/Hall Collins REG Dropbox/Hall Collins REG Team Folder/Code/ListingPacketCombiner"  
    "$HOME/Dropbox (Personal)/Hall Collins REG Team Folder/Code/ListingPacketCombiner"
    "$HOME/Desktop/ListingPacketCombiner"
    "$HOME/Downloads/ListingPacketCombiner"
)

found_location=""

for path in "${dropbox_paths[@]}"; do
    echo "🔍 Checking: $path"
    if [ -d "$path" ]; then
        echo "✅ FOUND APP FOLDER: $path"
        found_location="$path"
        
        echo "   📋 Contents:"
        check_path "$path/ultra_simple_combiner.py" "   Main App File"
        check_path "$path/Hall Collins Listing Packet Combiner.command" "   App Launcher"
        check_path "$path/templates" "   Templates Folder"
        
        if [ -f "$path/ultra_simple_combiner.py" ]; then
            echo ""
            echo "🎯 SOLUTION FOUND!"
            echo "   The app files are located at: $path"
            echo ""
            echo "✅ WHAT TO DO:"
            echo "   1. Open Finder"
            echo "   2. Navigate to: $path"
            echo "   3. Double-click: Hall Collins Listing Packet Combiner.command"
            echo ""
            break
        fi
    else
        echo "   ❌ Not found"
    fi
    echo ""
done

if [ -z "$found_location" ]; then
    echo "❌ APP FOLDER NOT FOUND IN COMMON LOCATIONS"
    echo ""
    echo "🔧 TROUBLESHOOTING STEPS:"
    echo ""
    echo "1. 📱 CHECK DROPBOX SYNC:"
    echo "   • Open Dropbox app"
    echo "   • Look for sync status"
    echo "   • Make sure files are downloaded (no cloud icons)"
    echo ""
    echo "2. 🔍 SEARCH FOR FILES:"
    echo "   • Open Finder"
    echo "   • Press Cmd+F to search"
    echo "   • Search for: ultra_simple_combiner.py"
    echo ""
    echo "3. 📁 CHECK DROPBOX FOLDER:"
    echo "   • Open Dropbox in web browser"
    echo "   • Navigate to: Hall Collins REG Team Folder/Code"
    echo "   • Download the ListingPacketCombiner folder"
    echo ""
    echo "4. 📞 CONTACT SUPPORT:"
    echo "   • Take screenshot of this diagnostic"
    echo "   • Include your Dropbox sync status"
    echo ""
fi

# Additional system information
echo "💻 SYSTEM INFO:"
echo "   🍎 macOS Version: $(sw_vers -productVersion)"
echo "   👤 User: $(whoami)"
echo "   🏠 Home: $HOME"
echo ""

# Check Dropbox installation
if command -v dropbox &> /dev/null; then
    echo "✅ Dropbox command line tool found"
elif [ -d "/Applications/Dropbox.app" ]; then
    echo "✅ Dropbox app found in Applications"
else
    echo "⚠️  Dropbox may not be properly installed"
fi

echo ""
read -p "Press Enter to close this diagnostic..."
