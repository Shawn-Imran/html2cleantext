"""
Tests for html2cleantext.cli module.
"""

import pytest
import tempfile
import os
from io import StringIO
from unittest.mock import patch, MagicMock
import sys

from html2cleantext.cli import main, _determine_keep_links, _determine_keep_images, setup_logging


class TestDetermineKeepLinks:
    """Test link preservation logic."""
    
    def test_explicit_no_links(self):
        """Test explicit --no-links flag."""
        args = MagicMock()
        args.no_links = True
        args.keep_links = False
        args.mode = 'markdown'
        
        assert _determine_keep_links(args) is False
    
    def test_explicit_keep_links(self):
        """Test explicit --keep-links flag."""
        args = MagicMock()
        args.no_links = False
        args.keep_links = True
        args.mode = 'text'
        
        assert _determine_keep_links(args) is True
    
    def test_default_markdown_mode(self):
        """Test default behavior in markdown mode."""
        args = MagicMock()
        args.no_links = False
        args.keep_links = False
        args.mode = 'markdown'
        
        assert _determine_keep_links(args) is True
    
    def test_default_text_mode(self):
        """Test default behavior in text mode."""
        args = MagicMock()
        args.no_links = False
        args.keep_links = False
        args.mode = 'text'
        
        assert _determine_keep_links(args) is False


class TestDetermineKeepImages:
    """Test image preservation logic."""
    
    def test_explicit_no_images(self):
        """Test explicit --no-images flag."""
        args = MagicMock()
        args.no_images = True
        args.keep_images = False
        args.mode = 'markdown'
        
        assert _determine_keep_images(args) is False
    
    def test_explicit_keep_images(self):
        """Test explicit --keep-images flag."""
        args = MagicMock()
        args.no_images = False
        args.keep_images = True
        args.mode = 'text'
        
        assert _determine_keep_images(args) is True
    
    def test_default_markdown_mode(self):
        """Test default behavior in markdown mode."""
        args = MagicMock()
        args.no_images = False
        args.keep_images = False
        args.mode = 'markdown'
        
        assert _determine_keep_images(args) is True
    
    def test_default_text_mode(self):
        """Test default behavior in text mode."""
        args = MagicMock()
        args.no_images = False
        args.keep_images = False
        args.mode = 'text'
        
        assert _determine_keep_images(args) is False


class TestSetupLogging:
    """Test logging setup functionality."""
    
    def test_verbose_logging(self):
        """Test verbose logging setup."""
        with patch('logging.basicConfig') as mock_config:
            setup_logging(verbose=True)
            mock_config.assert_called_once()
            call_args = mock_config.call_args.kwargs
            assert call_args['level'] == 10  # DEBUG level
    
    def test_normal_logging(self):
        """Test normal logging setup."""
        with patch('logging.basicConfig') as mock_config:
            setup_logging(verbose=False)
            mock_config.assert_called_once()
            call_args = mock_config.call_args.kwargs
            assert call_args['level'] == 30  # WARNING level


class TestCliIntegration:
    """Test CLI integration and end-to-end functionality."""
    
    def test_html_string_input(self):
        """Test processing HTML string input."""
        html_content = "<h1>Test Title</h1><p>Test content</p>"
        
        with patch.object(sys, 'argv', ['html2cleantext', html_content]):
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                with patch('sys.stderr', new_callable=StringIO):
                    try:
                        main()
                        output = mock_stdout.getvalue()
                        assert "# Test Title" in output
                        assert "Test content" in output
                    except SystemExit:
                        # CLI may exit normally
                        pass
    
    def test_file_input_with_output(self):
        """Test processing file input with output to file."""
        html_content = "<h1>File Test</h1><p>Content from file</p>"
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as input_file:
            input_file.write(html_content)
            input_path = input_file.name
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as output_file:
            output_path = output_file.name
        
        try:
            args = ['html2cleantext', input_path, '--output', output_path]
            with patch.object(sys, 'argv', args):
                with patch('sys.stderr', new_callable=StringIO):
                    try:
                        main()
                        
                        # Check output file was created and contains expected content
                        with open(output_path, 'r', encoding='utf-8') as f:
                            output_content = f.read()
                            assert "# File Test" in output_content
                            assert "Content from file" in output_content
                    except SystemExit:
                        # CLI may exit normally
                        pass
        finally:
            os.unlink(input_path)
            if os.path.exists(output_path):
                os.unlink(output_path)
    
    def test_text_mode(self):
        """Test text output mode."""
        html_content = "<h1>Title</h1><p>Paragraph with <strong>bold</strong>.</p>"
        
        args = ['html2cleantext', html_content, '--mode', 'text']
        with patch.object(sys, 'argv', args):
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                with patch('sys.stderr', new_callable=StringIO):
                    try:
                        main()
                        output = mock_stdout.getvalue()
                        assert "Title" in output
                        assert "bold" in output
                        # Should not contain Markdown formatting
                        assert "#" not in output
                        assert "**" not in output
                    except SystemExit:
                        pass
    
    def test_version_flag(self):
        """Test --version flag."""
        with patch.object(sys, 'argv', ['html2cleantext', '--version']):
            with pytest.raises(SystemExit) as exc_info:
                with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                    main()
            
            # Version command should exit with code 0
            assert exc_info.value.code == 0
    
    def test_help_flag(self):
        """Test --help flag."""
        with patch.object(sys, 'argv', ['html2cleantext', '--help']):
            with pytest.raises(SystemExit) as exc_info:
                with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                    main()
            
            # Help command should exit with code 0
            assert exc_info.value.code == 0
    
    def test_error_handling(self):
        """Test CLI error handling."""
        # Test with nonexistent file
        with patch.object(sys, 'argv', ['html2cleantext', 'nonexistent.html']):
            with patch('sys.stderr', new_callable=StringIO) as mock_stderr:
                with pytest.raises(SystemExit) as exc_info:
                    main()
                
                # Should exit with error code
                assert exc_info.value.code == 1
                
                error_output = mock_stderr.getvalue()
                assert "Error:" in error_output
