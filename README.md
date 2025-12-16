# Hall Collins Listing Packet Combiner

A native macOS application for combining PDF files from MLS listing downloads into professional listing packets.

## Features
- ✅ **Native macOS App** with custom flower icon
- ✅ **ZIP File Support** - Automatically extracts ZIP downloads from MLS
- ✅ **PDF Combination** - Combines multiple PDFs while skipping cover pages
- ✅ **Address-Based Naming** - Creates packets named "123 Address - Packet.pdf"
- ✅ **Downloads Output** - Saves finished packets to your Downloads folder
- ✅ **Working GUI** - Uses Python 3.11 with Tk 8.6 for visible Entry widgets

## Quick Start

### Option 1: App Bundle (Recommended)
1. Double-click `ListingPacketCombiner.app`
2. Drag to your Dock for easy access
3. Shows beautiful flower icon in Dock

### Option 2: Command Launcher
1. Double-click `ListingPacketCombiner.command`
2. Opens in Terminal and launches GUI

## Usage
1. **Select Files**: Click "Select PDF or ZIP Files" or use "Quick: Browse Downloads"
2. **Enter Address**: Type the property address (e.g., "123 Main Street")
3. **Create Packet**: Click "Create Listing Packet" button
4. **Find Output**: Check your Downloads folder for the finished packet

## Files in This Folder
- `ListingPacketCombiner.app` - Main macOS application bundle with icon
- `listing_packet_combiner_working.py` - Python application code
- `ListingPacketCombiner.command` - Alternative command line launcher
- `setup_icon.sh` - Script to regenerate app icon from flower_icon1.png
- `flower_icon1.png` - Current app icon source image
- `app_icon.icns` - Generated macOS app icon file

## Requirements
- Python 3.11 (for working tkinter Entry widgets)
- PyPDF2 (automatically installed if missing)

## Icon Updates
To update the app icon:
1. Replace `flower_icon1.png` with your new image
2. Run `./setup_icon.sh` to regenerate the icon
3. The app will automatically use the new icon

## Technical Notes
- Uses Python 3.11 specifically for Tk 8.6 compatibility
- Avoids Python 3.9.6 which has Entry widget visibility issues on macOS
- No virtual environment needed - uses system Python 3.11
- Automatically handles ZIP extraction and temporary file cleanup
