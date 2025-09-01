"""
html2cleantext - Convert HTML to clean, structured Markdown or plain text.

A Python package for extracting readable content from HTML sources with robust
boilerplate removal, language-specific normalization, and flexible output formats.
"""

from .core import to_markdown, to_text

__version__ = "0.1.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

# Expose the main API functions
__all__ = ["to_markdown", "to_text"]
