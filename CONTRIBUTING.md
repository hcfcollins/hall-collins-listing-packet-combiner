# Contributing to Hall Collins Listing Packet Combiner

Thank you for your interest in contributing to the Hall Collins Listing Packet Combiner! This document provides guidelines for contributing to this project.

## 🏗️ Development Setup

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/hall-collins-listing-packet-combiner.git
   cd hall-collins-listing-packet-combiner
   ```
3. **Run setup**:
   ```bash
   ./SETUP\ -\ Run\ This\ First.command
   ```

## 🔄 Development Workflow

1. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** following the coding standards below

3. **Test your changes**:
   - Run the application: `./Hall\ Collins\ Listing\ Packet\ Combiner.command`
   - Test with various PDF/ZIP files
   - Verify cover page and Instagram post generation
   - Check error handling

4. **Commit your changes**:
   ```bash
   git add .
   git commit -m "feat: add your feature description"
   ```

5. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create a Pull Request** on GitHub

## 📋 Coding Standards

### Python Code Style
- Follow PEP 8 guidelines
- Use meaningful variable names
- Add docstrings to functions and classes
- Handle exceptions gracefully
- Add DEBUG print statements for troubleshooting

### Example Function Structure:
```python
def your_function(param1, param2):
    """Brief description of what the function does.
    
    Args:
        param1 (str): Description of param1
        param2 (int): Description of param2
        
    Returns:
        bool: Description of return value
    """
    try:
        # Your code here
        print(f"DEBUG: Processing {param1}")
        result = some_operation(param1, param2)
        return True
    except Exception as e:
        print(f"DEBUG: Error in your_function: {e}")
        return False
```

### Shell Scripts
- Include shebang line: `#!/bin/bash`
- Add comments explaining complex operations
- Include error handling
- Provide user feedback with echo statements

## 🧪 Testing

### Manual Testing Checklist
- [ ] Application launches successfully
- [ ] PDF files can be selected and processed
- [ ] ZIP files are extracted correctly
- [ ] JPG files convert to PDF properly
- [ ] Cover pages generate with correct branding
- [ ] Instagram posts create successfully
- [ ] Output files save to Downloads folder
- [ ] Error messages are user-friendly
- [ ] All GUI elements are visible and functional

### Test Files
Create test files in `test_files/` directory (not committed to repo):
- Sample PDFs of various sizes
- ZIP files containing PDFs
- JPG images for cover pages
- Edge cases (corrupted files, empty ZIPs, etc.)

## 📝 Commit Message Guidelines

Use conventional commit format:
- `feat:` - New features
- `fix:` - Bug fixes
- `docs:` - Documentation changes
- `style:` - Code style changes (formatting, etc.)
- `refactor:` - Code refactoring
- `test:` - Adding tests
- `chore:` - Maintenance tasks

Examples:
- `feat: add support for DOCX file conversion`
- `fix: resolve GUI freezing on large ZIP files`
- `docs: update installation instructions`

## 🐛 Bug Reports

When reporting bugs, please include:

1. **Environment details**:
   - macOS version
   - Python version
   - Library versions (run diagnostic command)

2. **Steps to reproduce**:
   - Exact steps taken
   - Files used (if possible)
   - Screenshots if GUI-related

3. **Expected vs actual behavior**

4. **Error messages** (check terminal output)

## 💡 Feature Requests

For new features:

1. **Check existing issues** to avoid duplicates
2. **Describe the use case** clearly
3. **Explain the benefits** to real estate agents
4. **Consider implementation complexity**

## 🔒 Security Considerations

- **Never commit** sensitive information (API keys, passwords, personal data)
- **Be careful with file paths** - use relative paths when possible
- **Validate user input** properly
- **Handle file permissions** correctly

## 📁 Project Structure

```
├── ultra_simple_combiner.py     # Main application logic
├── templates/                   # Hall Collins branding assets
├── *.command                   # macOS launcher scripts
├── requirements.txt            # Python dependencies
├── README.md                   # Main documentation
└── docs/                       # Additional documentation
```

## 🚀 Release Process

1. Update version numbers in relevant files
2. Update CHANGELOG.md with new features/fixes
3. Test thoroughly with real-world scenarios
4. Create release tag: `git tag -a v1.2.0 -m "Version 1.2.0"`
5. Push tags: `git push --tags`
6. Create GitHub release with release notes

## 📞 Getting Help

- Check existing documentation and issues first
- Use descriptive titles and detailed descriptions
- Provide context about your real estate workflow
- Be patient and respectful

## 📄 License

By contributing, you agree that your contributions will be licensed under the same terms as the project.

---

Thank you for helping make the Hall Collins Listing Packet Combiner even better! 🏡✨
