"""
HTML cleaning and language normalization functions.
"""

import re
import logging
from bs4 import BeautifulSoup, Tag
from readability import Document
from typing import Optional
from .utils import detect_language

logger = logging.getLogger(__name__)


def remove_links(soup: BeautifulSoup) -> BeautifulSoup:
    """
    Remove all links from the HTML while preserving the text content.
    
    Args:
        soup (BeautifulSoup): Parsed HTML document
        
    Returns:
        BeautifulSoup: Modified soup with links removed
    """
    # Find all anchor tags and replace them with their text content
    for link in soup.find_all('a'):
        # Replace the link with its text content
        if link.string:
            link.replace_with(link.get_text())
        else:
            link.unwrap()  # Remove tag but keep children
    
    return soup


def remove_images(soup: BeautifulSoup) -> BeautifulSoup:
    """
    Remove all images from the HTML.
    
    Args:
        soup (BeautifulSoup): Parsed HTML document
        
    Returns:
        BeautifulSoup: Modified soup with images removed
    """
    # Remove img tags
    for img in soup.find_all('img'):
        img.decompose()
    
    # Remove picture tags and their content
    for picture in soup.find_all('picture'):
        picture.decompose()
    
    # Remove figure tags that only contain images
    for figure in soup.find_all('figure'):
        if not figure.get_text().strip():
            figure.decompose()
    
    return soup


def strip_boilerplate(soup: BeautifulSoup, use_readability: bool = True) -> BeautifulSoup:
    """
    Remove boilerplate content like navigation, footers, sidebars, and ads.
    
    Args:
        soup (BeautifulSoup): Parsed HTML document
        use_readability (bool): Whether to use readability-lxml for content extraction
        
    Returns:
        BeautifulSoup: Modified soup with boilerplate removed
    """
    if use_readability:
        try:
            # Use readability to extract main content
            html_str = str(soup)
            doc = Document(html_str)
            clean_html = doc.summary()
            soup = BeautifulSoup(clean_html, 'lxml')
        except Exception as e:
            logger.warning(f"Readability extraction failed, using manual cleaning: {e}")
            soup = _manual_boilerplate_removal(soup)
    else:
        soup = _manual_boilerplate_removal(soup)
    
    return soup


def _manual_boilerplate_removal(soup: BeautifulSoup) -> BeautifulSoup:
    """
    Manually remove common boilerplate elements.
    
    Args:
        soup (BeautifulSoup): Parsed HTML document
        
    Returns:
        BeautifulSoup: Modified soup with boilerplate removed
    """
    # Common boilerplate selectors
    boilerplate_selectors = [
        'nav', 'header', 'footer', 'aside', 'sidebar',
        '.nav', '.navigation', '.navbar', '.menu',
        '.header', '.footer', '.sidebar', '.aside',
        '.advertisement', '.ads', '.ad', '.banner',
        '.social', '.share', '.sharing',
        '.comments', '.comment-section',
        '.breadcrumb', '.breadcrumbs',
        '#nav', '#navigation', '#navbar', '#menu',
        '#header', '#footer', '#sidebar', '#aside',
        '#advertisement', '#ads', '#ad', '#banner',
        '#social', '#share', '#sharing',
        '#comments', '#comment-section',
        '#breadcrumb', '#breadcrumbs'
    ]
    
    # Remove elements by selector
    for selector in boilerplate_selectors:
        for element in soup.select(selector):
            element.decompose()
    
    # Remove elements by common attributes
    for element in soup.find_all(attrs={'role': ['navigation', 'banner', 'contentinfo', 'complementary']}):
        element.decompose()
    
    # Remove script and style tags
    for script in soup.find_all(['script', 'style', 'noscript']):
        script.decompose()
    
    # Remove elements with low text-to-html ratio (likely boilerplate)
    _remove_low_content_elements(soup)
    
    return soup


def _remove_low_content_elements(soup: BeautifulSoup, threshold: float = 0.3) -> None:
    """
    Remove elements that have a low text-to-HTML ratio, indicating they're likely boilerplate.
    
    Args:
        soup (BeautifulSoup): Parsed HTML document
        threshold (float): Minimum text-to-HTML ratio to keep an element
    """
    for element in soup.find_all(['div', 'section', 'article']):
        if isinstance(element, Tag):
            text_length = len(element.get_text().strip())
            html_length = len(str(element))
            
            if html_length > 0 and text_length / html_length < threshold and text_length < 50:
                element.decompose()


def normalize_language(text: str, lang: Optional[str] = None) -> str:
    """
    Normalize text based on language-specific rules.
    
    Args:
        text (str): Text to normalize
        lang (str, optional): Language code. If None, will auto-detect.
        
    Returns:
        str: Normalized text
    """
    if not text or not isinstance(text, str):
        return ""
    
    try:
        # Auto-detect language if not provided
        if lang is None:
            lang = detect_language(text)
        
        # Apply language-specific normalization
        if lang == 'bn':  # Bengali
            text = _normalize_bengali(text)
        elif lang == 'en':  # English
            text = _normalize_english(text)
        
        # General normalization for all languages
        text = _general_normalization(text)
        
    except Exception as e:
        logger.warning(f"Language normalization failed: {e}")
        # Fall back to basic normalization
        text = _general_normalization(text)
    
    return text


def _normalize_bengali(text: str) -> str:
    """
    Apply Bengali-specific text normalization.
    
    Args:
        text (str): Bengali text to normalize
        
    Returns:
        str: Normalized Bengali text
    """
    # Normalize Bengali punctuation and spacing
    text = re.sub(r'[\u0964\u0965]+', '।', text)  # Normalize devanagari punctuation
    text = re.sub(r'[\u09F7\u09F8\u09F9]+', '', text)  # Remove Bengali currency symbols
    
    # Normalize zero-width characters common in Bengali
    text = re.sub(r'[\u200C\u200D]+', '', text)  # Remove zero-width non-joiner/joiner
    
    return text


def _normalize_english(text: str) -> str:
    """
    Apply English-specific text normalization.
    
    Args:
        text (str): English text to normalize
        
    Returns:
        str: Normalized English text
    """
    # Normalize common English punctuation issues
    text = re.sub(r'[“”]', '"', text)  # Smart quotes to regular quotes
    text = re.sub(r'[‘’]', "'", text)  # Smart apostrophes to regular apostrophes
    text = re.sub(r'[–—]', '-', text)  # Em/en dashes to hyphens
    text = re.sub(r'…', '...', text)  # Ellipsis character to three dots
    
    return text


def _general_normalization(text: str) -> str:
    """
    Apply general text normalization for all languages.
    
    Args:
        text (str): Text to normalize
        
    Returns:
        str: Normalized text
    """
    # Remove excessive whitespace
    text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)  # Multiple newlines to double newlines
    text = re.sub(r'[ \t]+', ' ', text)  # Multiple spaces/tabs to single space
    
    # Remove trailing whitespace from lines
    text = '\n'.join(line.rstrip() for line in text.split('\n'))
    
    # Remove common Unicode control characters
    text = re.sub(r'[\u00A0\u2000-\u200F\u2028-\u202F\u205F-\u206F\uFEFF]', ' ', text)
    
    return text.strip()


def clean_html_attributes(soup: BeautifulSoup) -> BeautifulSoup:
    """
    Remove unnecessary HTML attributes and inline styles.
    
    Args:
        soup (BeautifulSoup): Parsed HTML document
        
    Returns:
        BeautifulSoup: Modified soup with cleaned attributes
    """
    # Attributes to keep for semantic meaning
    keep_attributes = ['href', 'src', 'alt', 'title', 'colspan', 'rowspan']
    
    for element in soup.find_all(True):  # Find all tags
        if hasattr(element, 'attrs'):
            # Remove style attributes
            if 'style' in element.attrs:
                del element.attrs['style']
            
            # Remove class and id attributes (usually for styling)
            if 'class' in element.attrs:
                del element.attrs['class']
            if 'id' in element.attrs:
                del element.attrs['id']
            
            # Remove other attributes not in keep list
            attrs_to_remove = [attr for attr in element.attrs.keys() 
                             if attr not in keep_attributes]
            for attr in attrs_to_remove:
                del element.attrs[attr]
    
    return soup
