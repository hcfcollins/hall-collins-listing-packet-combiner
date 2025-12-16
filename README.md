# 🏡 Hall Collins Listing Packet Combiner

A professional real estate listing packet creator for macOS. This application combines multiple PDF files, ZIP downloads from MLS systems, and JPG images into professional listing packets with Hall Collins branding.

## ✨ Features

- 📄 **PDF Combining** - Merge multiple PDFs into one professional packet
- 📁 **ZIP File Support** - Automatically extracts and processes ZIP downloads from MLS
- 🖼️ **JPG to PDF Conversion** - Convert JPG images to PDF and include in packets
- 🏠 **Custom Cover Pages** - Generate branded cover pages with property photos and addresses
- 📱 **Instagram Posts** - Create social media posts (New Listing, Under Contract, Sold)
- 🎯 **Smart Addressing** - Automatic address parsing and packet naming
- 💾 **Downloads Integration** - Saves finished packets directly to Downloads folder
- 🖥️ **Native macOS GUI** - User-friendly interface with proper macOS integration

## 🚀 Quick Start

### First Time Setup
1. **Double-click** `SETUP - Run This First.command`
2. **Wait** for setup to complete (installs required Python libraries)
3. **Close** the Terminal window when done

### Using the App
1. **Double-click** `Hall Collins Listing Packet Combiner.command`
2. **Select** your PDF, JPG, or ZIP files
3. **Enter** property address (optional for basic combining)
4. **Select** property photo for cover page and Instagram posts
5. **Click** "Create Listing Packet"

## 📁 Project Structure

```
ListingPacketCombiner/
├── 📄 ultra_simple_combiner.py          # Main Python application
├── 🚀 Hall Collins Listing Packet Combiner.command  # App launcher
├── ⚙️ SETUP - Run This First.command     # One-time setup script
├── 📋 requirements.txt                   # Python dependencies
├── 📖 README.md                          # This file
├── 🎨 hall_collins_logo.png             # Company logo
└── 📁 templates/                         # Branding assets (do not modify)
    ├── 1) HC - Template Bottom Photo.png
    ├── HC_Solid White Logo_Transparent Back.png
    ├── Instagram New Post Template.png
    ├── Instagram Sold Post Template.png
    └── Instagram Under Contract Post Template.png
```

## 🛠️ Requirements

- **macOS** (tested on macOS 10.15+)
- **Python 3.11+** (automatically checked during setup)
- **Internet connection** (for initial library installation)

### Python Dependencies
- `PyPDF2` - PDF manipulation
- `reportlab` - PDF generation 
- `Pillow` - Image processing
- `tkinter` - GUI (included with Python)

## 🔧 Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/hall-collins-listing-packet-combiner.git
   cd hall-collins-listing-packet-combiner
   ```

2. **Run setup:**
   ```bash
   ./SETUP\ -\ Run\ This\ First.command
   ```

3. **Launch the app:**
   ```bash
   ./Hall\ Collins\ Listing\ Packet\ Combiner.command
   ```

## 📖 Usage Guide

### Basic PDF Combining
1. Open the application
2. Click "📁 Select PDF, JPG or ZIP Files"
3. Choose your files
4. Click "🔗 Create Listing Packet"
5. Find your packet in the Downloads folder

### Professional Packets with Cover Page
1. Follow steps 1-3 above
2. Enter the **Street Address** and **City, State**
3. Click "📸 Select Property Photo"
4. Check "✅ Include Cover Page"
5. Optionally check "📱 Create Instagram Posts"
6. Click "🔗 Create Listing Packet"

## 📱 Social Media Features

When enabled, the app creates three Instagram-ready posts:
- **New Listing** - Announce new properties
- **Under Contract** - Show pending sales
- **Sold** - Celebrate closed deals

All posts include your property photo and Hall Collins branding.

## 🔍 Troubleshooting

### Common Issues
- **GUI elements not visible**: Run `INSTALL_REQUIREMENTS.command`
- **Python not found**: Install Python 3.11+ from [python.org](https://python.org)
- **Files not found**: Ensure all template files are in the `templates/` folder

### Diagnostic Tools
- `DIAGNOSE_SYSTEM.command` - System health check
- `FIND_APP_FILES.command` - Locate missing files
- `TROUBLESHOOTING - Missing GUI Elements.md` - GUI issues

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is proprietary software of Hall Collins Real Estate Group.

## 📞 Support

For technical support or questions:
- Check the troubleshooting documentation
- Run diagnostic commands
- Contact Hall Collins IT support
