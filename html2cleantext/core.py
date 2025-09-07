"""
Core functions for converting HTML to clean Markdown or plain text.
"""

import os
import logging
from bs4 import BeautifulSoup
from markdownify import markdownify
from typing import Union, Optional

from .utils import fetch_url, is_url, is_file_path, normalize_whitespace, format_readable_text
from .cleaners import (
    remove_links, 
    remove_images, 
    strip_boilerplate, 
    normalize_language,
    clean_html_attributes,
    replace_images_with_text,
    group_product_info
)

logger = logging.getLogger(__name__)


def to_markdown(
    html_input: Union[str, os.PathLike], 
    keep_links: bool = True,
    keep_images: bool = True, 
    remove_boilerplate: bool = True,
    normalize_lang: bool = True,
    language: Optional[str] = None,
    readable_format: bool = True
) -> str:
    """
    Convert HTML to clean Markdown format.
    
    Args:
        html_input: HTML string, file path, or URL
        keep_links: Whether to preserve links in the output (default: True)
        keep_images: Whether to preserve images in the output (default: True)
        remove_boilerplate: Whether to remove navigation, footers, etc. (default: True)
        normalize_lang: Whether to apply language-specific normalization (default: True)
        language: Language code for normalization (auto-detected if None)
        readable_format: Whether to format for human readability with proper paragraphs (default: True)
        
    Returns:
        str: Clean Markdown text
        
    Raises:
        ValueError: If input is invalid
        FileNotFoundError: If file path doesn't exist
        requests.RequestException: If URL fetching fails
    """
    # Get HTML content
    html_content = _get_html_content(html_input)
    
    # Parse HTML
    soup = BeautifulSoup(html_content, 'lxml')
    
    # Clean HTML attributes first
    soup = clean_html_attributes(soup)

    # Apply cleaning options
    if remove_boilerplate:
        soup = strip_boilerplate(soup)

    if not keep_links:
        soup = remove_links(soup)
    else:
        # If keep_links is True, convert <a> tags to Markdown links [text](URL)
        for a_tag in soup.find_all('a', href=True):
            link_text = a_tag.get_text().strip()
            link_url = a_tag['href']
            # Replace with Markdown link format
            replacement = f"[{link_text}]({link_url})" if link_text else f"[{link_url}]({link_url})"
            a_tag.replace_with(replacement)

    if not keep_images:
        soup = remove_images(soup)

    # Convert to Markdown
    markdown_text = markdownify(
        str(soup), 
        heading_style="ATX",  # Use # style headers
        bullets="*"  # Use * for bullet points
    )
    
    # Apply language normalization
    if normalize_lang:
        markdown_text = normalize_language(markdown_text, language)
    
    # Final cleanup
    if readable_format:
        markdown_text = format_readable_text(markdown_text)
    else:
        markdown_text = normalize_whitespace(markdown_text)
    
    return markdown_text


def to_text(
    html_input: Union[str, os.PathLike],
    keep_links: bool = False,
    keep_images: bool = False,
    remove_boilerplate: bool = True,
    normalize_lang: bool = True,
    language: Optional[str] = None,
    readable_format: bool = True
) -> str:
    """
    Convert HTML to clean plain text format.
    
    Args:
        html_input: HTML string, file path, or URL
        keep_links: Whether to preserve links in the output (default: False)
        keep_images: Whether to preserve images in the output (default: False)
        remove_boilerplate: Whether to remove navigation, footers, etc. (default: True)
        normalize_lang: Whether to apply language-specific normalization (default: True)
        language: Language code for normalization (auto-detected if None)
        readable_format: Whether to format for human readability with proper paragraphs (default: True)
        
    Returns:
        str: Clean plain text
        
    Raises:
        ValueError: If input is invalid
        FileNotFoundError: If file path doesn't exist
        requests.RequestException: If URL fetching fails
    """
    # Get HTML content
    html_content = _get_html_content(html_input)
    
    # Parse HTML
    soup = BeautifulSoup(html_content, 'lxml')
    
    # Clean HTML attributes first
    soup = clean_html_attributes(soup)
    
    # Apply cleaning options
    if remove_boilerplate:
        soup = strip_boilerplate(soup)

    # FIXED: Handle images properly based on keep_images flag
    if keep_images:
        # Replace images with text placeholders instead of removing them
        # Extract base URL if input was a URL
        base_url = ""
        if is_url(str(html_input)):
            base_url = str(html_input)

        soup = replace_images_with_text(soup, base_url)
    else:
        # Remove images completely
        soup = remove_images(soup)

    if not keep_links:
        soup = remove_links(soup)
    else:
        # If keep_links is True, replace <a> tags with their text and URL in [Link:URL] format
        for a_tag in soup.find_all('a', href=True):
            link_text = a_tag.get_text().strip()
            link_url = a_tag['href']
            if link_text:
                replacement = f"{link_text} [Link:{link_url}]"
            else:
                replacement = f"[Link:{link_url}]"
            a_tag.replace_with(replacement)

    # image_urls = [img.get("src") for img in soup.find_all("img") if img.get("src")]
    # for url in image_urls:
    #     print(url)

    # Extract text content with better paragraph preservation
    if readable_format:
        # Replace block elements with their text + appropriate newlines
        block_elements = ['p', 'div', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li', 'blockquote', 'article', 'section', 'br']
        found_blocks = soup.find_all(block_elements)

        for tag in found_blocks:
            if tag.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                # Headers get double newlines before and after
                tag.replace_with(f"\n\n{tag.get_text().strip()}\n\n")
            elif tag.name in ['p', 'div', 'li', 'blockquote', 'article', 'section']:
                # Paragraphs get newlines after
                tag.replace_with(f"{tag.get_text().strip()}\n\n")
            elif tag.name == 'br':
                tag.replace_with("\n")

        text = soup.get_text(separator=' ', strip=True)
    else:
        text = soup.get_text(separator=' ', strip=True)
    
    # Apply language normalization
    if normalize_lang:
        text = normalize_language(text, language)
    
    # Final cleanup
    if readable_format:
        text = format_readable_text(text)
    else:
        text = normalize_whitespace(text)
    # Group product/category/brand info into paragraphs
    text = group_product_info(text)

    return text


def _get_html_content(html_input: Union[str, os.PathLike]) -> str:
    """
    Get HTML content from string, file, or URL.
    
    Args:
        html_input: HTML string, file path, or URL
        
    Returns:
        str: HTML content
        
    Raises:
        ValueError: If input type is not supported
        FileNotFoundError: If file doesn't exist
        requests.RequestException: If URL fetching fails
    """
    if not html_input:
        return ""
    
    html_input_str = str(html_input)
    
    # Check if it's a URL
    if is_url(html_input_str):
        logger.info(f"Fetching HTML from URL: {html_input_str}")
        return fetch_url(html_input_str)
    
    # Check if it's a file path
    elif is_file_path(html_input_str) and os.path.exists(html_input_str):
        logger.info(f"Reading HTML from file: {html_input_str}")
        try:
            with open(html_input_str, 'r', encoding='utf-8') as f:
                return f.read()
        except UnicodeDecodeError:
            # Try with different encoding if UTF-8 fails
            with open(html_input_str, 'r', encoding='latin-1') as f:
                return f.read()
    
    # Check if file path exists but file doesn't
    elif is_file_path(html_input_str):
        raise FileNotFoundError(f"File not found: {html_input_str}")
    
    # Assume it's raw HTML content
    else:
        logger.info("Processing raw HTML content")
        return html_input_str


def from_file(file_path: Union[str, os.PathLike], **kwargs) -> str:
    """
    Convenience function to convert HTML file to clean text/markdown.
    
    Args:
        file_path: Path to HTML file
        **kwargs: Additional arguments passed to to_markdown() or to_text()
        
    Returns:
        str: Clean text or markdown
    """
    return to_markdown(file_path, **kwargs)


def from_url(url: str, **kwargs) -> str:
    """
    Convenience function to convert HTML from URL to clean text/markdown.
    
    Args:
        url: URL to fetch HTML from
        **kwargs: Additional arguments passed to to_markdown() or to_text()
        
    Returns:
        str: Clean text or markdown
    """
    return to_markdown(url, **kwargs)
