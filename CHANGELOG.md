# Changelog

All notable changes to the html2cleantext project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-09-01

### Added
- **Core functionality**:
  - `to_markdown()` function for converting HTML to clean Markdown
  - `to_text()` function for converting HTML to plain text
  - Support for HTML strings, file paths, and URLs as input

- **HTML cleaning and processing**:
  - Intelligent boilerplate removal using readability-lxml
  - Manual boilerplate removal fallback
  - Link preservation/removal options
  - Image preservation/removal options
  - HTML attribute cleaning (removes styles, classes, IDs)
  - Script and style tag removal

- **Language support**:
  - Automatic language detection using langdetect
  - Bengali language normalization (zero-width character removal, punctuation)
  - English language normalization (smart quotes, em-dashes, ellipsis)
  - General text normalization for all languages

- **Command-line interface**:
  - Full CLI with argparse
  - Support for all package features via command line
  - Multiple output modes (markdown, text)
  - File input/output with UTF-8 encoding
  - Verbose logging option

- **Utility functions**:
  - URL fetching with proper headers
  - File path detection and validation
  - Whitespace normalization
  - Error handling and logging

- **Testing and examples**:
  - Comprehensive test suite with 66+ tests
  - Unit tests for all modules (core, utils, cleaners, cli)
  - Example scripts demonstrating usage patterns
  - Batch processing examples
  - CLI usage demonstrations

### Technical Details
- **Dependencies**: beautifulsoup4, lxml, markdownify, readability-lxml, langdetect, requests
- **Python support**: 3.7+
- **Architecture**: Modular design with clean separation of concerns
- **Error handling**: Graceful fallbacks and informative error messages
- **Unicode support**: Full UTF-8 support for international content

### Package Structure
```
html2cleantext/
├── html2cleantext/
│   ├── __init__.py          # Main package interface
│   ├── core.py              # Core conversion functions
│   ├── cleaners.py          # HTML cleaning and language normalization
│   ├── utils.py             # Utility functions
│   └── cli.py               # Command-line interface
├── tests/                   # Comprehensive test suite
│   ├── test_core.py
│   ├── test_cleaners.py
│   ├── test_utils.py
│   └── test_cli.py
├── examples/                # Usage examples
│   ├── basic_usage.py
│   ├── batch_processing.py
│   └── cli_examples.py
├── README.md                # Documentation
├── requirements.txt         # Dependencies
├── setup.py                 # Package setup
├── pyproject.toml          # Modern Python packaging
└── LICENSE                  # MIT License
```

### Features Highlights
- 🧹 **Smart Cleaning**: Removes navigation, footers, ads automatically
- 📝 **Flexible Output**: Markdown or plain text formats
- 🌍 **Language-Aware**: Special support for Bengali and English
- 🔗 **Link Control**: Configurable link and image handling
- 🚀 **Multiple Sources**: Process strings, files, or URLs
- ⚡ **CLI & API**: Both programmatic and command-line interfaces
- 📦 **Modern Package**: Follows Python packaging best practices
