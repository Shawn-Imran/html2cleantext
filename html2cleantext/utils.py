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
