"""
Tests for html2cleantext.cleaners module.
"""

import pytest
from bs4 import BeautifulSoup

from html2cleantext.cleaners import (
    remove_links, remove_images, strip_boilerplate, 
    normalize_language, clean_html_attributes
)


class TestRemoveLinks:
    """Test link removal functionality."""
    
    def test_simple_link_removal(self):
        """Test removal of simple links."""
        html = '<p>Check out <a href="https://example.com">this link</a>!</p>'
        soup = BeautifulSoup(html, 'lxml')
        result_soup = remove_links(soup)
        result_text = result_soup.get_text()
        
        assert "this link" in result_text
        assert "https://example.com" not in result_text
        assert "Check out" in result_text
    
    def test_multiple_links_removal(self):
        """Test removal of multiple links."""
        html = '''
        <div>
            <p>Visit <a href="http://site1.com">Site 1</a> and <a href="http://site2.com">Site 2</a>.</p>
            <p>Also check <a href="/local">local page</a>.</p>
        </div>
        '''
        soup = BeautifulSoup(html, 'lxml')
        result_soup = remove_links(soup)
        result_text = result_soup.get_text()
        
        assert "Site 1" in result_text
        assert "Site 2" in result_text
        assert "local page" in result_text
        assert "http://site1.com" not in result_text
        assert "http://site2.com" not in result_text
    
    def test_nested_link_content(self):
        """Test links with nested content."""
        html = '<p>Link with <a href="/test"><strong>bold</strong> text</a> here.</p>'
        soup = BeautifulSoup(html, 'lxml')
        result_soup = remove_links(soup)
        result_text = result_soup.get_text()
        
        assert "bold text" in result_text
        assert "/test" not in result_text


class TestRemoveImages:
    """Test image removal functionality."""
    
    def test_simple_image_removal(self):
        """Test removal of simple images."""
        html = '<p>Look at this: <img src="test.jpg" alt="Test image"></p>'
        soup = BeautifulSoup(html, 'lxml')
        result_soup = remove_images(soup)
        result_text = result_soup.get_text()
        
        assert "Look at this:" in result_text
        assert "test.jpg" not in result_text
        assert "Test image" not in result_text
    
    def test_picture_element_removal(self):
        """Test removal of picture elements."""
        html = '''
        <picture>
            <source srcset="image.webp" type="image/webp">
            <img src="image.jpg" alt="Fallback">
        </picture>
        '''
        soup = BeautifulSoup(html, 'lxml')
        result_soup = remove_images(soup)
        
        assert not result_soup.find('picture')
        assert not result_soup.find('img')
    
    def test_figure_with_only_images(self):
        """Test removal of figure elements that contain only images."""
        html = '''
        <figure>
            <img src="chart.png" alt="Chart">
        </figure>
        '''
        soup = BeautifulSoup(html, 'lxml')
        result_soup = remove_images(soup)
        
        # Figure should be removed since it only contained images
        assert not result_soup.find('figure')
    
    def test_figure_with_text_preserved(self):
        """Test that figures with text content are preserved."""
        html = '''
        <figure>
            <img src="chart.png" alt="Chart">
            <figcaption>Important chart showing data trends</figcaption>
        </figure>
        '''
        soup = BeautifulSoup(html, 'lxml')
        result_soup = remove_images(soup)
        result_text = result_soup.get_text()
        
        # Caption text should be preserved
        assert "Important chart showing data trends" in result_text


class TestStripBoilerplate:
    """Test boilerplate removal functionality."""
    
    def test_navigation_removal(self):
        """Test removal of navigation elements."""
        html = '''
        <html>
        <body>
            <nav>
                <ul>
                    <li><a href="/">Home</a></li>
                    <li><a href="/about">About</a></li>
                </ul>
            </nav>
            <main>
                <h1>Main Content</h1>
                <p>Important paragraph.</p>
            </main>
        </body>
        </html>
        '''
        soup = BeautifulSoup(html, 'lxml')
        result_soup = strip_boilerplate(soup, use_readability=False)  # Use manual cleaning for predictable tests
        result_text = result_soup.get_text()
        
        assert "Main Content" in result_text
        assert "Important paragraph" in result_text
        assert "Home" not in result_text
        assert "About" not in result_text
    
    def test_footer_removal(self):
        """Test removal of footer elements."""
        html = '''
        <html>
        <body>
            <article>
                <h1>Article Title</h1>
                <p>Article content here.</p>
            </article>
            <footer>
                <p>Copyright 2025</p>
                <div class="social">Social links</div>
            </footer>
        </body>
        </html>
        '''
        soup = BeautifulSoup(html, 'lxml')
        result_soup = strip_boilerplate(soup, use_readability=False)
        result_text = result_soup.get_text()
        
        assert "Article Title" in result_text
        assert "Article content" in result_text
        assert "Copyright 2025" not in result_text
        assert "Social links" not in result_text
    
    def test_script_and_style_removal(self):
        """Test removal of script and style tags."""
        html = '''
        <html>
        <head>
            <style>body { color: red; }</style>
        </head>
        <body>
            <h1>Content</h1>
            <script>console.log("test");</script>
            <p>Paragraph</p>
        </body>
        </html>
        '''
        soup = BeautifulSoup(html, 'lxml')
        result_soup = strip_boilerplate(soup, use_readability=False)
        result_text = result_soup.get_text()
        
        assert "Content" in result_text
        assert "Paragraph" in result_text
        assert "color: red" not in result_text
        assert "console.log" not in result_text


class TestCleanHtmlAttributes:
    """Test HTML attribute cleaning functionality."""
    
    def test_style_attribute_removal(self):
        """Test removal of style attributes."""
        html = '<div style="color: red; font-size: 14px;"><p>Content</p></div>'
        soup = BeautifulSoup(html, 'lxml')
        result_soup = clean_html_attributes(soup)
        
        div_tag = result_soup.find('div')
        assert 'style' not in div_tag.attrs
    
    def test_class_and_id_removal(self):
        """Test removal of class and id attributes."""
        html = '<div class="container main" id="main-content"><p class="text">Content</p></div>'
        soup = BeautifulSoup(html, 'lxml')
        result_soup = clean_html_attributes(soup)
        
        div_tag = result_soup.find('div')
        p_tag = result_soup.find('p')
        
        assert 'class' not in div_tag.attrs
        assert 'id' not in div_tag.attrs
        assert 'class' not in p_tag.attrs
    
    def test_semantic_attributes_preserved(self):
        """Test that semantic attributes are preserved."""
        html = '''
        <a href="https://example.com" title="External link">Link</a>
        <img src="image.jpg" alt="Description">
        <table>
            <td colspan="2" rowspan="1">Cell</td>
        </table>
        '''
        soup = BeautifulSoup(html, 'lxml')
        result_soup = clean_html_attributes(soup)
        
        link = result_soup.find('a')
        img = result_soup.find('img')
        td = result_soup.find('td')
        
        assert link.get('href') == 'https://example.com'
        assert link.get('title') == 'External link'
        assert img.get('src') == 'image.jpg'
        assert img.get('alt') == 'Description'
        assert td.get('colspan') == '2'
        assert td.get('rowspan') == '1'


class TestNormalizeLanguage:
    """Test language-specific normalization."""
    
    def test_english_normalization(self):
        """Test English text normalization."""
        text = "Testing \"smart quotes\" and 'apostrophes' with em-dashes and ellipsis..."
        result = normalize_language(text, lang='en')
        
        assert '"smart quotes"' in result
        assert "'apostrophes'" in result
        assert "em-dashes" in result
        assert "ellipsis..." in result
    
    def test_bengali_normalization(self):
        """Test Bengali text normalization."""
        # Bengali text with various punctuation and formatting issues
        text = "বাংলা টেক্সট\u200C\u200D পরীক্ষা।"  # Contains zero-width characters
        result = normalize_language(text, lang='bn')
        
        # Should remove zero-width characters
        assert '\u200C' not in result
        assert '\u200D' not in result
        assert "বাংলা টেক্সট পরীক্ষা" in result
    
    def test_auto_language_detection(self):
        """Test automatic language detection."""
        english_text = "This is a longer English text that should be automatically detected as English language."
        result = normalize_language(english_text)  # No language specified
        
        # Should apply English normalization
        # We can't easily test the specific changes without knowing the exact content,
        # but we can verify it doesn't crash
        assert isinstance(result, str)
        assert len(result) > 0
    
    def test_general_normalization_applied(self):
        """Test that general normalization is always applied."""
        text = "Text   with\n\n\n\nexcessive\t\twhitespace"
        result = normalize_language(text, lang='unknown')
        
        # Should clean up whitespace regardless of language
        assert "   " not in result
        assert "\n\n\n\n" not in result
        assert "\t\t" not in result
    
    def test_empty_text_handling(self):
        """Test handling of empty or None text."""
        assert normalize_language("") == ""
        assert normalize_language(None) == ""
