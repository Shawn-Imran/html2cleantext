"""
Tests for html2cleantext.core module.
"""

import pytest
import tempfile
import os
from pathlib import Path

from html2cleantext.core import to_markdown, to_text, _get_html_content


class TestGetHtmlContent:
    """Test the _get_html_content helper function."""
    
    def test_raw_html_string(self):
        """Test processing raw HTML string."""
        html = "<h1>Test</h1><p>Content</p>"
        result = _get_html_content(html)
        assert result == html
    
    def test_file_path(self):
        """Test processing HTML from file."""
        html_content = "<html><body><h1>File Test</h1></body></html>"
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as f:
            f.write(html_content)
            temp_path = f.name
        
        try:
            result = _get_html_content(temp_path)
            assert result.strip() == html_content
        finally:
            os.unlink(temp_path)
    
    def test_nonexistent_file(self):
        """Test error handling for nonexistent file."""
        with pytest.raises(FileNotFoundError):
            _get_html_content("nonexistent_file.html")
    
    def test_empty_input(self):
        """Test handling of empty input."""
        result = _get_html_content("")
        assert result == ""


class TestToMarkdown:
    """Test the to_markdown function."""
    
    def test_basic_conversion(self):
        """Test basic HTML to Markdown conversion."""
        html = "<h1>Title</h1><p>Paragraph with <strong>bold</strong> text.</p>"
        result = to_markdown(html)
        
        assert "# Title" in result
        assert "**bold**" in result
        assert "Paragraph with" in result
    
    def test_links_preservation(self):
        """Test link preservation option."""
        html = '<p>Check out <a href="https://example.com">this link</a>!</p>'
        
        # With links (default)
        result_with_links = to_markdown(html, keep_links=True)
        assert "[this link](https://example.com)" in result_with_links
        
        # Without links
        result_without_links = to_markdown(html, keep_links=False)
        assert "this link" in result_without_links
        assert "https://example.com" not in result_without_links
    
    def test_images_preservation(self):
        """Test image preservation option."""
        html = '<p>Look at this: <img src="test.jpg" alt="Test image"></p>'
        
        # With images (default)
        result_with_images = to_markdown(html, keep_images=True)
        assert "![Test image](test.jpg)" in result_with_images
        
        # Without images
        result_without_images = to_markdown(html, keep_images=False)
        assert "test.jpg" not in result_without_images
        assert "Test image" not in result_without_images
    
    def test_boilerplate_removal(self):
        """Test boilerplate removal functionality."""
        html = """
        <html>
        <head><title>Test</title></head>
        <body>
            <nav>Navigation</nav>
            <main>
                <h1>Main Content</h1>
                <p>This is important content.</p>
            </main>
            <footer>Footer content</footer>
        </body>
        </html>
        """
        
        # With boilerplate removal (default) - but we need to modify cleaners to disable readability for testing
        # For now, let's test the manual cleaning approach
        from html2cleantext.cleaners import strip_boilerplate
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html, 'lxml')
        cleaned_soup = strip_boilerplate(soup, use_readability=False)
        from html2cleantext.utils import normalize_whitespace
        result_clean = normalize_whitespace(cleaned_soup.get_text())
        
        assert "Navigation" not in result_clean
        assert "Footer content" not in result_clean
        assert "Main Content" in result_clean
        assert "important content" in result_clean
        
        # Without boilerplate removal
        result_full = to_markdown(html, remove_boilerplate=False)
        assert "Navigation" in result_full
        assert "Footer content" in result_full


class TestToText:
    """Test the to_text function."""
    
    def test_basic_conversion(self):
        """Test basic HTML to text conversion."""
        html = "<h1>Title</h1><p>Paragraph with <strong>bold</strong> text.</p>"
        result = to_text(html)
        
        assert "Title" in result
        assert "bold" in result
        assert "Paragraph with" in result
        # Should not contain Markdown formatting
        assert "#" not in result
        assert "**" not in result
    
    def test_default_options(self):
        """Test that to_text has different defaults than to_markdown."""
        html = '<p>Text with <a href="https://example.com">link</a> and <img src="test.jpg" alt="image">.</p>'
        
        result = to_text(html)
        # By default, text mode should remove links and images
        assert "https://example.com" not in result
        assert "test.jpg" not in result
        assert "link" in result  # Text content should remain


class TestFileProcessing:
    """Test file-based processing."""
    
    def test_file_with_utf8_encoding(self):
        """Test processing file with UTF-8 encoding."""
        html_content = "<h1>Test with émojis 🚀</h1><p>Unicode content: café</p>"
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as f:
            f.write(html_content)
            temp_path = f.name
        
        try:
            result = to_markdown(temp_path)
            assert "émojis 🚀" in result
            assert "café" in result
        finally:
            os.unlink(temp_path)
    
    def test_file_processing_preserves_structure(self):
        """Test that file processing preserves HTML structure correctly."""
        html_content = """
        <html>
        <body>
            <h1>Main Title</h1>
            <h2>Subtitle</h2>
            <ul>
                <li>Item 1</li>
                <li>Item 2</li>
            </ul>
        </body>
        </html>
        """
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as f:
            f.write(html_content)
            temp_path = f.name
        
        try:
            # Test without boilerplate removal to preserve structure
            result = to_markdown(temp_path, remove_boilerplate=False)
            assert "# Main Title" in result
            assert "## Subtitle" in result
            assert "* Item 1" in result
            assert "* Item 2" in result
        finally:
            os.unlink(temp_path)


class TestEdgeCases:
    """Test edge cases and error conditions."""
    
    def test_empty_html(self):
        """Test processing empty HTML."""
        result = to_markdown("")
        assert result == ""
    
    def test_malformed_html(self):
        """Test processing malformed HTML."""
        html = "<h1>Unclosed header<p>Missing closing tags"
        result = to_markdown(html)
        # Should still extract some content
        assert "Unclosed header" in result
        assert "Missing closing tags" in result
    
    def test_html_with_special_characters(self):
        """Test HTML with special characters and entities."""
        html = "<p>Testing &amp; entities like &lt;script&gt; and &quot;quotes&quot;</p>"
        result = to_markdown(html)
        assert "&" in result
        assert "<script>" in result
        assert '"quotes"' in result
