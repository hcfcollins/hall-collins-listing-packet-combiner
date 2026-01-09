# Changelog

All notable changes to the Hall Collins Listing Packet Combiner will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Future feature planning and development

## [2.4.0] - 2026-01-09

### Added
- 🔄 Refresh button for processing multiple properties without restarting the app
- 📥 Recent Downloads section for quick file selection from Downloads folder
- Double-click to select files from recent downloads list
- Automatic refresh of recent files when starting new property

### Enhanced
- User workflow improvements for real estate agents handling multiple listings
- Quick access to recently downloaded files without opening Finder
- File size display and smart filename truncation in recent downloads
- Seamless multi-property workflow for busy agents

### Features
- Recent downloads listbox shows PDF, ZIP, and JPG files
- Manual refresh button (🔄) to update downloads list
- File type icons (📄📁📷) for easy file identification
- Support for files up to Downloads folder capacity
- Auto-sorting by most recent modification time

## [2.1.0] - 2026-01-09

### Added
- 🔄 Refresh button for processing multiple properties without restarting the app
- 📥 Recent Downloads section for quick file selection from Downloads folder
- Double-click to select files from recent downloads list
- Automatic refresh of recent files when starting new property

### Enhanced
- User workflow improvements for real estate agents handling multiple listings
- Quick access to recently downloaded files without opening Finder
- File size display and smart filename truncation in recent downloads
- Seamless multi-property workflow for busy agents

### Features
- Recent downloads listbox shows PDF, ZIP, and JPG files
- Manual refresh button (🔄) to update downloads list
- File type icons (📄📁📷) for easy file identification
- Support for files up to Downloads folder capacity
- Auto-sorting by most recent modification time

## [2.0.0] - 2024-12-16

### Added
- Instagram post generation (New Listing, Under Contract, Sold)
- Enhanced cover page creation with Hall Collins branding
- Support for JPG to PDF conversion
- Professional template integration
- Improved error handling and user feedback
- Diagnostic and troubleshooting tools
- Comprehensive setup automation

### Features
- 📄 PDF combining and merging
- 📁 ZIP file extraction and processing
- 🖼️ JPG to PDF conversion
- 🏠 Custom cover page generation
- 📱 Social media post creation
- 🎯 Smart address parsing
- 💾 Downloads folder integration
- 🖥️ Native macOS GUI

### Fixed
- GUI element visibility issues on macOS
- Python 3.11 compatibility for tkinter
- File path handling improvements
- Memory management for large files

### Technical
- Python 3.11+ requirement for stable tkinter
- ReportLab for PDF generation
- Pillow for image processing
- PyPDF2 for PDF manipulation
- Cross-platform file handling

## [1.0.0] - 2024-08-07

### Added
- Initial release of basic PDF combiner
- macOS application bundle support
- Basic GUI with file selection
- Address-based naming
- ZIP file support
- Downloads folder output

### Features
- Basic PDF combining functionality
- ZIP extraction capabilities
- Simple address parsing
- macOS native launcher scripts
- Hall Collins branding integration

---

## Release Notes

### Version 2.0.0 Highlights
This major release focuses on professional real estate agent workflows:

🎨 **Professional Branding**: Full Hall Collins template integration
📱 **Social Media Ready**: Automatic Instagram post generation  
🏠 **Cover Pages**: Beautiful property cover pages with photos
🔧 **Better Setup**: Automated installation and diagnostics
📊 **Enhanced UX**: Improved GUI and error handling

### Upgrade Notes
- Run `SETUP - Run This First.command` after updating
- New Python dependencies will be installed automatically
- Template files must remain in `templates/` folder
- Instagram posts require property photo selection

### Known Issues
- Large ZIP files (>100MB) may cause temporary GUI freezing
- Some PDF files with complex encryption may not merge properly
- Instagram post generation requires all template PNG files

### Support
- Run diagnostic commands for troubleshooting
- Check template file integrity
- Verify Python 3.11+ installation
