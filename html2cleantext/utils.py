"""
Utility functions for html2cleantext package.
"""

import requests
from langdetect import detect, DetectorFactory, LangDetectException
from typing import Optional
import logging

# Set seed for consistent language detection results
DetectorFactory.seed = 0

logger = logging.getLogger(__name__)


def fetch_url(url: str, timeout: int = 30, headers: Optional[dict] = None) -> str:
    """
    Fetch HTML content from a URL.
    
    Args:
        url (str): The URL to fetch
        timeout (int): Request timeout in seconds (default: 30)
        headers (dict, optional): Custom headers for the request
        
    Returns:
        str: HTML content from the URL
        
    Raises:
        requests.RequestException: If the request fails
        ValueError: If the URL is invalid
    """
    if not url or not isinstance(url, str):
        raise ValueError("URL must be a non-empty string")
    
    # Default headers to mimic a browser request
    default_headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    if headers:
        default_headers.update(headers)
    
    try:
        response = requests.get(url, timeout=timeout, headers=default_headers)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        logger.error(f"Failed to fetch URL {url}: {e}")
        raise


def detect_language(text: str) -> Optional[str]:
    """
    Detect the language of the given text.
    
    Args:
        text (str): Text to analyze for language detection
        
    Returns:
        str or None: Language code (e.g., 'en', 'bn') or None if detection fails
    """
    if not text or not isinstance(text, str):
        return None
    
    # Clean text for better detection - remove extra whitespace
    cleaned_text = ' '.join(text.split())
    
    # Need at least some text for reliable detection
    if len(cleaned_text.strip()) < 10:
        return None
    
    try:
        detected_lang = detect(cleaned_text)
        logger.debug(f"Detected language: {detected_lang}")
        return detected_lang
    except LangDetectException as e:
        logger.warning(f"Language detection failed: {e}")
        return None


def is_url(text: str) -> bool:
    """
    Check if a string is a valid URL.
    
    Args:
        text (str): String to check
        
    Returns:
        bool: True if the string appears to be a URL
    """
    if not text or not isinstance(text, str):
        return False
    
    text = text.strip().lower()
    return text.startswith(('http://', 'https://', 'ftp://'))


def is_file_path(text: str) -> bool:
    """
    Check if a string appears to be a file path.
    
    Args:
        text (str): String to check
        
    Returns:
        bool: True if the string appears to be a file path
    """
    if not text or not isinstance(text, str):
        return False
    
    # Don't treat HTML content as file paths
    if text.strip().startswith('<'):
        return False
    
    # Don't treat URLs as file paths
    if is_url(text):
        return False
    
    import os
    text = text.strip()
    
    # Check if it's a single token (no spaces) and has file-like characteristics
    if len(text.split()) != 1:
        return False
    
    # Check for file extension
    if '.' in text and text.split('.')[-1].isalpha():
        return True
    
    # Check for path separators
    if os.sep in text or '/' in text or '\\' in text:
        return True
    
    # If it exists as a file, it's definitely a file path
    if os.path.exists(text):
        return True
    
    return False


def normalize_whitespace(text: str) -> str:
    """
    Normalize whitespace in text by collapsing multiple spaces and newlines.
    
    Args:
        text (str): Text to normalize
        
    Returns:
        str: Text with normalized whitespace
    """
    if not text:
        return ""
    
    # Replace multiple whitespace characters with single spaces
    import re
    normalized = re.sub(r'\s+', ' ', text.strip())
    return normalized


def format_readable_text(text: str) -> str:
    """
    Format text for human readability with proper paragraphs and line breaks.
    Preserves URLs and image placeholders without adding spaces.
    
    Args:
        text (str): Text to format
        
    Returns:
        str: Human-readable formatted text with proper paragraphs
    """
    if not text:
        return ""
    
    import re
    
    # First, protect URLs and image placeholders from space normalization
    url_pattern = r'(https?://[^\s\]]+|[^\s\]]*\.[a-zA-Z]{2,}[^\s\]]*)'
    image_pattern = r'(\[IMAGE:[^\]]+\])'
    
    # Find all URLs and image placeholders
    protected_items = []
    
    def protect_item(match):
        item = match.group(0)
        placeholder = f"__PROTECTED_ITEM_{len(protected_items)}__"
        protected_items.append(item)
        return placeholder
    
    # Protect URLs and image placeholders
    text = re.sub(url_pattern, protect_item, text)
    text = re.sub(image_pattern, protect_item, text)
    
    # Now do normal text processing
    # Replace multiple spaces/tabs with single space
    text = re.sub(r'[ \t]+', ' ', text)
    
    # Convert single newlines within paragraphs to spaces, but preserve double newlines
    lines = text.split('\n')
    processed_lines = []
    
    for i, line in enumerate(lines):
        line = line.strip()
        if not line:  # Empty line
            processed_lines.append('')
        else:
            # Check if this line should be merged with the previous one
            if (processed_lines and 
                processed_lines[-1] and  # Previous line is not empty
                not line[0].isupper() and  # Current line doesn't start with capital
                not processed_lines[-1].endswith('.') and  # Previous line doesn't end with period
                not processed_lines[-1].endswith('!') and  # Previous line doesn't end with exclamation
                not processed_lines[-1].endswith('?') and  # Previous line doesn't end with question mark
                not processed_lines[-1].endswith(':') and  # Previous line doesn't end with colon
                len(processed_lines[-1]) > 20):  # Previous line is substantial
                # Merge with previous line
                processed_lines[-1] += ' ' + line
            else:
                processed_lines.append(line)
    
    text = '\n'.join(processed_lines)
    
    # Normalize line breaks - convert multiple newlines to paragraph breaks
    text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)
    
    # Split into paragraphs and clean each one
    paragraphs = text.split('\n\n')
    cleaned_paragraphs = []
    
    for paragraph in paragraphs:
        paragraph = paragraph.strip()
        if paragraph:  # Only keep non-empty paragraphs
            # Ensure sentences are properly spaced (but avoid URLs)
            paragraph = re.sub(r'\.(\w)', r'. \1', paragraph)  # Add space after period if missing
            paragraph = re.sub(r'\?(\w)', r'? \1', paragraph)  # Add space after question mark
            paragraph = re.sub(r'!(\w)', r'! \1', paragraph)   # Add space after exclamation
            
            # Remove excessive spaces within the paragraph (but preserve protected items)
            paragraph = re.sub(r' +', ' ', paragraph)
            
            cleaned_paragraphs.append(paragraph)
    
    # Join paragraphs with double newlines for clear separation
    result = '\n\n'.join(cleaned_paragraphs)
    
    # Restore protected URLs and image placeholders
    for i, item in enumerate(protected_items):
        placeholder = f"__PROTECTED_ITEM_{i}__"
        result = result.replace(placeholder, item)
    
    return result.strip()
