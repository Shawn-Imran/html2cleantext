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

CURRENCY_SYMBOLS_AND_CODES = [
    # Common currency symbols
    "€", "$", "£", "¥", "₹", "₽", "₩", "₺", "₫", "฿", "₴", "₦", "₲", "₡", "₵", "₸", "₭", "₠", "₢", "₳", "₥", "₧", "₯", "₰", "₱", "₲", "₳", "₴", "₵", "₸", "₺", "₼", "₾", "₿", "៛", "₪", "₠", "₡", "₢", "₣", "₤", "₥", "₦", "₧", "₨", "₩", "₪", "₫", "₭", "₮", "₯", "₰", "₱", "₲", "₳", "₴", "₵", "₸", "₺", "₼", "₾", "₿", "৳", "¤",
    # ISO 4217 currency codes
    "AED", "AFN", "ALL", "AMD", "ANG", "AOA", "ARS", "AUD", "AWG", "AZN", "BAM", "BBD", "BDT", "BGN", "BHD", "BIF", "BMD", "BND", "BOB", "BRL", "BSD", "BTN", "BWP", "BYN", "BZD", "CAD", "CDF", "CHF", "CLP", "CNY", "COP", "CRC", "CUC", "CUP", "CVE", "CZK", "DJF", "DKK", "DOP", "DZD", "EGP", "ERN", "ETB", "EUR", "FJD", "FKP", "GBP", "GEL", "GGP", "GHS", "GIP", "GMD", "GNF", "GTQ", "GYD", "HKD", "HNL", "HRK", "HTG", "HUF", "IDR", "ILS", "IMP", "INR", "IQD", "IRR", "ISK", "JMD", "JOD", "JPY", "KES", "KGS", "KHR", "KMF", "KPW", "KRW", "KWD", "KYD", "KZT", "LAK", "LBP", "LKR", "LRD", "LSL", "LYD", "MAD", "MDL", "MGA", "MKD", "MMK", "MNT", "MOP", "MRU", "MUR", "MVR", "MWK", "MXN", "MYR", "MZN", "NAD", "NGN", "NIO", "NOK", "NPR", "NZD", "OMR", "PAB", "PEN", "PGK", "PHP", "PKR", "PLN", "PYG", "QAR", "RON", "RSD", "RUB", "RWF", "SAR", "SBD", "SCR", "SDG", "SEK", "SGD", "SHP", "SLL", "SOS", "SPL", "SRD", "STN", "SVC", "SYP", "SZL", "THB", "TJS", "TMT", "TND", "TOP", "TRY", "TTD", "TVD", "TWD", "TZS", "UAH", "UGX", "USD", "UYU", "UZS", "VEF", "VES", "VND", "VUV", "WST", "XAF", "XAG", "XAU", "XCD", "XDR", "XOF", "XPD", "XPF", "XPT", "YER", "ZAR", "ZMW", "ZWD"
    # Add more as needed
]
currency_regex = "|".join([re.escape(c) for c in CURRENCY_SYMBOLS_AND_CODES])


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
    Preserves URLs and image placeholders.
    
    Args:
        text (str): Text to normalize
        
    Returns:
        str: Normalized text
    """
    # Protect URLs and image placeholders from normalization
    url_pattern = r'(https?://[^\s\]]+|[^\s\]]*\.[a-zA-Z]{2,}[^\s\]]*)'
    image_pattern = r'(\[IMAGE:[^\]]+\])'
    
    protected_items = []
    
    def protect_item(match):
        item = match.group(0)
        placeholder = f"__PROTECTED_ITEM_{len(protected_items)}__"
        protected_items.append(item)
        return placeholder
    
    # Protect URLs and image placeholders
    text = re.sub(url_pattern, protect_item, text)
    text = re.sub(image_pattern, protect_item, text)
    
    # Remove excessive whitespace
    text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)  # Multiple newlines to double newlines
    text = re.sub(r'[ \t]+', ' ', text)  # Multiple spaces/tabs to single space
    
    # Remove trailing whitespace from lines
    text = '\n'.join(line.rstrip() for line in text.split('\n'))
    
    # Remove common Unicode control characters
    text = re.sub(r'[\u00A0\u2000-\u200F\u2028-\u202F\u205F-\u206F\uFEFF]', ' ', text)
    
    # Restore protected URLs and image placeholders
    for i, item in enumerate(protected_items):
        placeholder = f"__PROTECTED_ITEM_{i}__"
        text = text.replace(placeholder, item)
    
    return text.strip()


def replace_images_with_text(soup: BeautifulSoup, base_url: str = "") -> BeautifulSoup:
    """
    Replace images with text placeholders containing the alt text and src URL.
    This preserves image information in plain text format when keep_images=True.

    Args:
        soup (BeautifulSoup): Parsed HTML document
        base_url (str): Base URL to prepend to relative URLs

    Returns:
        BeautifulSoup: Modified soup with images replaced by text placeholders
    """
    def _normalize_image_url(url: str) -> str:
        """Normalize URL by removing spaces and fixing common issues."""
        if not url:
            return ""
        # Remove spaces from URLs (including before file extensions)
        url = re.sub(r'\s+', '', url)
        # Handle relative URLs
        if base_url and not url.startswith(('http://', 'https://', '//')):
            if url.startswith('/'):
                # Absolute path
                base_parts = base_url.split('/')
                if len(base_parts) >= 3:
                    url = '/'.join(base_parts[0:3]) + url
            else:
                # Relative path
                base_for_relative = base_url
                if not base_for_relative.endswith('/'):
                    base_for_relative += '/'
                url = base_for_relative + url
        return url
    
    def _create_image_text(alt: str, title: str, src: str) -> str:
        """Create standardized image text representation (URL only, no alt/title/caption)."""
        src = _normalize_image_url(src)
        return f"[IMAGE:{src}]"

    # Extract CSS background images first
    _extract_css_background_images(soup, base_url)

    # Replace img tags with text placeholders
    for img in soup.find_all('img'):
        src = img.get('src', '')
        alt = img.get('alt', '')
        title = img.get('title', '')

        # print("image: ", src)
        image_text = _create_image_text(alt, title, src)
        img.replace_with(image_text)

    # Handle picture tags and their content
    for picture in soup.find_all('picture'):
        img_tag = picture.find('img')
        if img_tag:
            src = img_tag.get('src', '')
            alt = img_tag.get('alt', '')
            title = img_tag.get('title', '')

            image_text = _create_image_text(alt, title, src)
            picture.replace_with(image_text)
        else:
            picture.replace_with("[IMAGE:picture-element]")

    # Handle figure tags that contain images
    for figure in soup.find_all('figure'):
        img_tag = figure.find('img')
        if img_tag:
            src = img_tag.get('src', '')
            alt = img_tag.get('alt', '')
            title = img_tag.get('title', '')

            # Check for figcaption
            caption = figure.find('figcaption')
            if caption:
                caption_text = caption.get_text().strip()
                src = _normalize_image_url(src)
                image_text = f"[IMAGE:{caption_text}-{src}]"
            else:
                image_text = _create_image_text(alt, title, src)

            figure.replace_with(image_text)

    return soup


def _extract_css_background_images(soup: BeautifulSoup, base_url: str = "") -> None:
    """
    Extract CSS background images and add them as text placeholders.
    
    Args:
        soup (BeautifulSoup): Parsed HTML document
        base_url (str): Base URL to prepend to relative URLs
    """
    def _normalize_bg_url(url: str) -> str:
        """Normalize URL by removing spaces and fixing common issues."""
        if not url:
            return ""
        
        # Remove spaces from URLs
        url = url.replace(' ', '')
        
        # Handle relative URLs
        if base_url and not url.startswith(('http://', 'https://', '//')):
            if url.startswith('/'):
                # Absolute path
                base_parts = base_url.split('/')
                if len(base_parts) >= 3:
                    url = '/'.join(base_parts[0:3]) + url
            else:
                # Relative path
                base_for_relative = base_url
                if not base_for_relative.endswith('/'):
                    base_for_relative += '/'
                url = base_for_relative + url
        
        return url
    
    # Find all elements with style attributes
    for element in soup.find_all(attrs={'style': True}):
        style = element.get('style', '')
        
        # Extract background-image URLs using regex
        bg_matches = re.findall(r'background-image\s*:\s*url\s*\(\s*["\']?([^"\')\s]+)["\']?\s*\)', style, re.IGNORECASE)
        
        for bg_url in bg_matches:
            normalized_url = _normalize_bg_url(bg_url)
            # Get element text or tag name for context
            element_text = element.get_text().strip()[:50] if element.get_text().strip() else element.name
            
            # Add background image as text
            bg_text = f"[IMAGE:background-{element_text}-{normalized_url}]"
            
            # Insert the background image text at the beginning of the element
            if element.string:
                element.string = bg_text + " " + element.string
            else:
                element.insert(0, bg_text + " ")


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


def group_product_info(text: str) -> str:
    """Group product/category/brand info into paragraphs based on repetitive patterns and any currency."""
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    product_cards = []
    current_card = []
    price_pattern = re.compile(
        rf"(\d{{1,3}}(?:\.\d{{3}})*,\d{{2}}\s?(?:{currency_regex})?\s?\*?|ab\s?\d{{1,3}}(?:\.\d{{3}})*,\d{{2}}\s?(?:{currency_regex})?\s?\*?|Statt:\s?\d{{1,3}}(?:\.\d{{3}})*,\d{{2}}\s?(?:{currency_regex})?\s?\*?)"
    )
    last_was_price = False
    for line in lines:
        if price_pattern.search(line):
            current_card.append(line)
            last_was_price = True
        else:
            if last_was_price and current_card:
                product_cards.append(' '.join(current_card))
                current_card = []
            current_card.append(line)
            last_was_price = False
    if current_card:
        product_cards.append(' '.join(current_card))
    return '\n\n'.join(product_cards)
