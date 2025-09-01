"""
Tests for html2cleantext.utils module.
"""

import pytest
from unittest.mock import patch, Mock

from html2cleantext.utils import (
    fetch_url, detect_language, is_url, is_file_path, normalize_whitespace
)


class TestIsUrl:
    """Test URL detection function."""
    
    def test_valid_urls(self):
        """Test detection of valid URLs."""
        valid_urls = [
            "https://example.com",
            "http://test.org",
            "https://subdomain.example.com/path/to/page",
            "ftp://files.example.com",
            "HTTP://CAPS.COM",  # Should handle case insensitivity
        ]
        
        for url in valid_urls:
            assert is_url(url), f"Should detect {url} as a URL"
    
    def test_invalid_urls(self):
        """Test rejection of non-URLs."""
        invalid_urls = [
            "example.com",  # Missing protocol
            "www.example.com",  # Missing protocol
            "file.html",
            "/path/to/file",
            "<html>content</html>",
            "",
            None,
            123,
        ]
        
        for not_url in invalid_urls:
            assert not is_url(not_url), f"Should not detect {not_url} as a URL"


class TestIsFilePath:
    """Test file path detection function."""
    
    def test_valid_file_paths(self):
        """Test detection of valid file paths."""
        valid_paths = [
            "file.html",
            "document.txt",
            "path/to/file.html",
            "C:\\Users\\file.txt",
            "/home/user/document.md",
            "../relative/file.html",
        ]
        
        for path in valid_paths:
            assert is_file_path(path), f"Should detect {path} as a file path"
    
    def test_invalid_file_paths(self):
        """Test rejection of non-file-paths."""
        invalid_paths = [
            "<html>content</html>",  # HTML content
            "https://example.com",  # URL
            "just text with spaces",  # Text with spaces
            "",  # Empty string
            None,  # None
            123,  # Number
        ]
        
        for not_path in invalid_paths:
            assert not is_file_path(not_path), f"Should not detect {not_path} as a file path"
    
    @patch('os.path.exists')
    def test_existing_file_detection(self, mock_exists):
        """Test that existing files are detected as file paths."""
        mock_exists.return_value = True
        
        # Even without extension, if file exists, it should be detected
        assert is_file_path("somefile")
        mock_exists.assert_called_with("somefile")


class TestDetectLanguage:
    """Test language detection function."""
    
    def test_english_detection(self):
        """Test detection of English text."""
        english_text = "This is a sample English text with enough content for language detection."
        result = detect_language(english_text)
        assert result == 'en'
    
    def test_short_text_returns_none(self):
        """Test that very short text returns None."""
        short_text = "Hi"
        result = detect_language(short_text)
        assert result is None
    
    def test_empty_text_returns_none(self):
        """Test that empty text returns None."""
        assert detect_language("") is None
        assert detect_language(None) is None
        assert detect_language(123) is None
    
    @patch('html2cleantext.utils.detect')
    def test_detection_failure_handling(self, mock_detect):
        """Test handling of language detection failures."""
        from langdetect import LangDetectException
        mock_detect.side_effect = LangDetectException("error_code", "Detection failed")
        
        result = detect_language("Some text that fails detection")
        assert result is None


class TestNormalizeWhitespace:
    """Test whitespace normalization function."""
    
    def test_multiple_spaces(self):
        """Test collapsing multiple spaces."""
        text = "Text    with     multiple   spaces"
        result = normalize_whitespace(text)
        assert result == "Text with multiple spaces"
    
    def test_newlines_and_tabs(self):
        """Test handling of newlines and tabs."""
        text = "Text\twith\ttabs\nand\nnewlines"
        result = normalize_whitespace(text)
        assert result == "Text with tabs and newlines"
    
    def test_leading_trailing_whitespace(self):
        """Test removal of leading and trailing whitespace."""
        text = "   Text with padding   "
        result = normalize_whitespace(text)
        assert result == "Text with padding"
    
    def test_empty_string(self):
        """Test empty string handling."""
        assert normalize_whitespace("") == ""
        assert normalize_whitespace("   ") == ""


class TestFetchUrl:
    """Test URL fetching function."""
    
    @patch('html2cleantext.utils.requests.get')
    def test_successful_fetch(self, mock_get):
        """Test successful URL fetching."""
        mock_response = Mock()
        mock_response.text = "<html><body>Test content</body></html>"
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        result = fetch_url("https://example.com")
        assert result == "<html><body>Test content</body></html>"
        
        # Verify correct headers were used
        mock_get.assert_called_once()
        call_args = mock_get.call_args
        assert 'headers' in call_args.kwargs
        assert 'User-Agent' in call_args.kwargs['headers']
    
    @patch('html2cleantext.utils.requests.get')
    def test_request_failure(self, mock_get):
        """Test handling of request failures."""
        import requests
        mock_get.side_effect = requests.RequestException("Network error")
        
        with pytest.raises(requests.RequestException):
            fetch_url("https://example.com")
    
    def test_invalid_url_input(self):
        """Test validation of URL input."""
        with pytest.raises(ValueError):
            fetch_url("")
        
        with pytest.raises(ValueError):
            fetch_url(None)
    
    @patch('html2cleantext.utils.requests.get')
    def test_custom_headers(self, mock_get):
        """Test custom headers functionality."""
        mock_response = Mock()
        mock_response.text = "content"
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        custom_headers = {"Authorization": "Bearer token"}
        fetch_url("https://example.com", headers=custom_headers)
        
        # Verify custom headers were merged with defaults
        call_args = mock_get.call_args
        headers = call_args.kwargs['headers']
        assert 'Authorization' in headers
        assert 'User-Agent' in headers
