# Publishing html2cleantext to PyPI

This guide walks you through the complete process of publishing your html2cleantext package to the Python Package Index (PyPI).

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Pre-Publishing Checklist](#pre-publishing-checklist)
3. [Setup PyPI Accounts](#setup-pypi-accounts)
4. [Prepare Package for Publishing](#prepare-package-for-publishing)
5. [Build and Upload](#build-and-upload)
6. [Post-Publishing Steps](#post-publishing-steps)
7. [Troubleshooting](#troubleshooting)
8. [Future Updates](#future-updates)

## Prerequisites

### Required Tools
Install the necessary tools for building and uploading packages:

```bash
pip install --upgrade pip
pip install --upgrade build twine setuptools wheel
```

### Version Control (Recommended)
Initialize a git repository to track changes:

```bash
git init
git add .
git commit -m "Initial commit - html2cleantext v0.1.0"
```

## Pre-Publishing Checklist

### 1. Update Package Metadata
Before publishing, update the placeholder information in your package files:

#### `setup.py` and `__init__.py`
- [ ] Change `author="Your Name"` to your actual name
- [ ] Change `author_email="your.email@example.com"` to your email
- [ ] Update `url="https://github.com/yourusername/html2cleantext"` with your GitHub URL
- [ ] Update the `project_urls` in `setup.py` with your actual repository links

#### Example updates needed:
```python
# In setup.py
author="Imran Ahmed",  # Replace with your name
author_email="your.email@domain.com",  # Replace with your email
url="https://github.com/yourusername/html2cleantext",  # Your GitHub repo

# In html2cleantext/__init__.py
__author__ = "Imran Ahmed"  # Replace with your name
__email__ = "your.email@domain.com"  # Replace with your email
```

### 2. Choose a Unique Package Name
Check if the name `html2cleantext` is available on PyPI:

```bash
pip search html2cleantext
# OR visit https://pypi.org/project/html2cleantext/
```

If the name is taken, consider alternatives:
- `html-to-cleantext`
- `html2clean`
- `cleanhtml2text`
- `html-cleaner-text`

Update the package name in:
- `setup.py` (`name=` parameter)
- `pyproject.toml` (`name=` parameter)
- Documentation and README files

### 3. Verify Package Structure
Ensure your package has all required files:

```
html2cleantext/
├── html2cleantext/           # ✅ Main package directory
│   ├── __init__.py          # ✅ Package init with __version__
│   ├── core.py              # ✅ Core functionality
│   ├── cleaners.py          # ✅ Cleaning functions
│   ├── utils.py             # ✅ Utilities
│   └── cli.py               # ✅ CLI interface
├── tests/                   # ✅ Test suite
├── examples/                # ✅ Usage examples
├── README.md                # ✅ Main documentation
├── LICENSE                  # ✅ License file
├── setup.py                 # ✅ Package setup
├── pyproject.toml          # ✅ Modern packaging config
└── requirements.txt         # ✅ Dependencies
```

### 4. Run Quality Checks
Before publishing, ensure everything works:

```bash
# Run all tests
python -m pytest tests/ -v

# Test package import
python -c "import html2cleantext; print(html2cleantext.__version__)"

# Test CLI
python -m html2cleantext.cli test_example.html

# Test installation in clean environment (optional)
pip install -e .
```

## Setup PyPI Accounts

### 1. Create PyPI Account
1. Go to https://pypi.org/account/register/
2. Create an account with a strong password
3. Verify your email address

### 2. Create TestPyPI Account (Recommended)
TestPyPI lets you practice uploading without affecting the real PyPI:
1. Go to https://test.pypi.org/account/register/
2. Create an account (can use same credentials as PyPI)

### 3. Generate API Tokens
API tokens are more secure than passwords:

#### For PyPI:
1. Go to https://pypi.org/manage/account/
2. Scroll to "API tokens"
3. Click "Add API token"
4. Name: "html2cleantext-upload"
5. Scope: "Entire account" (or specific project after first upload)
6. **Save the token immediately** - you won't see it again!

#### For TestPyPI:
1. Go to https://test.pypi.org/manage/account/
2. Follow the same steps as above

### 4. Configure Authentication
Create a `.pypirc` file in your home directory:

**Windows:** `C:\Users\YourUsername\.pypirc`
**Mac/Linux:** `~/.pypirc`

```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-your-actual-token-here

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-your-test-token-here
```

**Security Note:** Keep this file secure and never commit it to version control!

## Prepare Package for Publishing

### 1. Final Version Check
Ensure your version is set correctly in:
- `html2cleantext/__init__.py`: `__version__ = "0.1.0"`
- `setup.py`: `version="0.1.0"`
- `pyproject.toml`: `version = "0.1.0"`

### 2. Update Long Description
Your `setup.py` already reads from `README.md`. Verify it looks good:

```bash
python setup.py --long-description
```

### 3. Validate Package Metadata
Check that your package metadata is correct:

```bash
python setup.py check --metadata --strict
```

## Build and Upload

### 1. Clean Previous Builds
Remove any previous build artifacts:

```bash
# Windows PowerShell
Remove-Item -Recurse -Force dist, build, *.egg-info -ErrorAction SilentlyContinue

# Windows Command Prompt
rmdir /s /q dist build
del /q *.egg-info

# Mac/Linux
rm -rf dist/ build/ *.egg-info/
```

### 2. Build the Package
Use the modern `build` tool:

```bash
python -m build
```

This creates:
- `dist/html2cleantext-0.1.0-py3-none-any.whl` (wheel distribution)
- `dist/html2cleantext-0.1.0.tar.gz` (source distribution)

### 3. Test Upload to TestPyPI (Recommended)
First, test your upload on TestPyPI:

```bash
python -m twine upload --repository testpypi dist/*
```

If successful, test installation from TestPyPI:

```bash
# Create a new virtual environment for testing
python -m venv test_env
# Windows
test_env\Scripts\activate
# Mac/Linux
source test_env/bin/activate

# Install from TestPyPI
pip install -i https://test.pypi.org/simple/ html2cleantext

# Test it works
python -c "import html2cleantext; print(html2cleantext.__version__)"
html2cleantext test_example.html

# Clean up
deactivate
rmdir /s test_env  # Windows
rm -rf test_env    # Mac/Linux
```

### 4. Upload to PyPI
If TestPyPI upload worked, upload to the real PyPI:

```bash
python -m twine upload dist/*
```

## Post-Publishing Steps

### 1. Verify Package on PyPI
1. Visit https://pypi.org/project/html2cleantext/
2. Check that all information displays correctly
3. Test the download link

### 2. Test Installation
```bash
# Test in a clean environment
pip install html2cleantext

# Verify it works
python -c "import html2cleantext; print('✅ Package installed successfully')"
html2cleantext --version
```

### 3. Update Documentation
- Add installation instructions to README
- Update any documentation with the correct PyPI package name
- Tag the release in version control:

```bash
git tag v0.1.0
git push origin v0.1.0
```

### 4. Announce Your Package
- Share on social media
- Post to relevant forums/communities
- Add to your portfolio/resume

## Troubleshooting

### Common Issues and Solutions

#### "Package name already exists"
- Choose a different name
- Check if the existing package is abandoned
- Contact PyPI admins if you believe you have rights to the name

#### "Invalid authentication credentials"
- Double-check your API token
- Ensure `.pypirc` file is correctly formatted
- Try using `--username __token__ --password your-token` directly

#### "Metadata validation failed"
- Run `python setup.py check --metadata --strict`
- Fix any warnings or errors
- Ensure all required fields are filled

#### "Upload failed with HTTP 400"
- Check that your package version doesn't already exist
- Ensure all files in `dist/` are for the same version
- Clean and rebuild if necessary

#### "README not displaying correctly"
- Ensure `long_description_content_type="text/markdown"` in setup.py
- Test your README.md renders correctly on GitHub first
- Check for any Markdown syntax issues

### Build Issues
If you encounter build errors:

```bash
# Update build tools
pip install --upgrade build setuptools wheel

# Check for syntax errors
python -m py_compile html2cleantext/*.py

# Validate package structure
python setup.py check
```

## Future Updates

### Versioning Strategy
Follow [Semantic Versioning](https://semver.org/):
- **MAJOR** version (1.0.0): Breaking changes
- **MINOR** version (0.2.0): New features, backward compatible
- **PATCH** version (0.1.1): Bug fixes, backward compatible

### Publishing Updates
For future versions:

1. **Update version numbers** in all relevant files
2. **Update CHANGELOG.md** with new features/fixes
3. **Run tests** to ensure everything works
4. **Build and upload** following the same process
5. **Tag the release** in version control

```bash
# Example for version 0.1.1
# 1. Update version in files
# 2. Update changelog
# 3. Test everything
python -m pytest tests/
# 4. Build
python -m build
# 5. Upload
python -m twine upload dist/*
# 6. Tag
git tag v0.1.1
git push origin v0.1.1
```

### Automation (Advanced)
Consider setting up GitHub Actions for automated publishing:
- Automatic testing on pull requests
- Automated PyPI uploads on tagged releases
- Multiple Python version testing

## Security Best Practices

1. **Use API tokens** instead of passwords
2. **Secure your .pypirc file** (don't commit to version control)
3. **Enable two-factor authentication** on your PyPI account
4. **Use project-scoped tokens** when possible
5. **Regularly rotate your API tokens**

## Quick Command Reference

```bash
# Build package
python -m build

# Upload to TestPyPI
python -m twine upload --repository testpypi dist/*

# Upload to PyPI
python -m twine upload dist/*

# Check package
python setup.py check --metadata --strict

# Test installation
pip install html2cleantext

# Clean build artifacts
rm -rf dist/ build/ *.egg-info/  # Mac/Linux
Remove-Item -Recurse -Force dist, build, *.egg-info  # Windows PowerShell
```

---

**🎉 Congratulations!** Once you follow this guide, your html2cleantext package will be available for anyone to install with `pip install html2cleantext`!

For questions or issues during publishing, refer to the [official PyPI documentation](https://packaging.python.org/tutorials/packaging-projects/) or reach out to the Python packaging community.
