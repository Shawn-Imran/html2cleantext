#!/usr/bin/env python3
"""
Basic usage examples for html2cleantext.

This script demonstrates the basic functionality of the html2cleantext package.
"""

import html2cleantext

def basic_string_conversion():
    """Demonstrate converting HTML strings to Markdown and text."""
    print("=== Basic String Conversion ===")
    
    html = """
    <h1>Welcome to My Blog</h1>
    <p>This is a <strong>sample blog post</strong> with some content.</p>
    <p>Check out this <a href="https://example.com">awesome website</a>!</p>
    <ul>
        <li>Feature 1</li>
        <li>Feature 2</li>
        <li>Feature 3</li>
    </ul>
    """
    
    # Convert to Markdown (default)
    markdown = html2cleantext.to_markdown(html)
    print("Markdown output:")
    print(markdown)
    print()
    
    # Convert to plain text
    text = html2cleantext.to_text(html)
    print("Plain text output:")
    print(text)
    print()


def link_and_image_control():
    """Demonstrate controlling links and images in output."""
    print("=== Link and Image Control ===")
    
    html = """
    <article>
        <h2>Product Review</h2>
        <p>This is an amazing product! <a href="/buy-now">Buy it now</a>.</p>
        <img src="product.jpg" alt="Product image">
        <p>Visit our <a href="https://store.com">store</a> for more info.</p>
    </article>
    """
    
    # Keep everything (default for Markdown)
    full_markdown = html2cleantext.to_markdown(html)
    print("With links and images:")
    print(full_markdown)
    print()
    
    # Remove links but keep images
    no_links = html2cleantext.to_markdown(html, keep_links=False)
    print("Without links:")
    print(no_links)
    print()
    
    # Remove both links and images
    clean_text = html2cleantext.to_text(html)  # Text mode removes both by default
    print("Plain text (no links/images):")
    print(clean_text)
    print()


def boilerplate_removal():
    """Demonstrate boilerplate removal functionality."""
    print("=== Boilerplate Removal ===")
    
    html = """
    <html>
    <head><title>News Article</title></head>
    <body>
        <nav>
            <a href="/">Home</a> | <a href="/news">News</a> | <a href="/contact">Contact</a>
        </nav>
        
        <article>
            <h1>Breaking News: Important Discovery</h1>
            <p>Scientists have made an important discovery that will change everything.</p>
            <p>This breakthrough has significant implications for the future.</p>
        </article>
        
        <aside>
            <h3>Related Articles</h3>
            <ul>
                <li><a href="/article1">Article 1</a></li>
                <li><a href="/article2">Article 2</a></li>
            </ul>
        </aside>
        
        <footer>
            <p>&copy; 2025 News Site. All rights reserved.</p>
            <div class="social">Follow us on social media!</div>
        </footer>
    </body>
    </html>
    """
    
    # With boilerplate removal (default)
    clean = html2cleantext.to_markdown(html)
    print("With boilerplate removal:")
    print(clean)
    print()
    
    # Without boilerplate removal
    full = html2cleantext.to_markdown(html, remove_boilerplate=False)
    print("Without boilerplate removal:")
    print(full)
    print()


def file_processing():
    """Demonstrate processing HTML files."""
    print("=== File Processing ===")
    
    # Create a temporary HTML file
    import tempfile
    import os
    
    html_content = """
    <!DOCTYPE html>
    <html>
    <head><title>Sample Document</title></head>
    <body>
        <h1>Document Title</h1>
        <p>This content was loaded from a file.</p>
        <blockquote>
            Important quote that should be preserved in the output.
        </blockquote>
    </body>
    </html>
    """
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as f:
        f.write(html_content)
        temp_path = f.name
    
    try:
        # Process the file
        result = html2cleantext.to_markdown(temp_path)
        print(f"Processed file {temp_path}:")
        print(result)
        print()
        
    finally:
        os.unlink(temp_path)


def language_specific_processing():
    """Demonstrate language-specific processing."""
    print("=== Language-Specific Processing ===")
    
    # English content with smart quotes
    english_html = '<p>This text has "smart quotes" and apostrophes like these.</p>'
    english_result = html2cleantext.to_text(english_html, language='en')
    print("English normalization:")
    print(f"Original: {english_html}")
    print(f"Normalized: {english_result}")
    print()
    
    # Bengali content
    bengali_html = '<p>এই একটি বাংলা বাক্য।\u200C কিছু বিশেষ অক্ষর।</p>'
    bengali_result = html2cleantext.to_text(bengali_html, language='bn')
    print("Bengali normalization:")
    print(f"Original: {bengali_html}")
    print(f"Normalized: {bengali_result}")
    print()


if __name__ == "__main__":
    print("html2cleantext - Basic Usage Examples")
    print("=" * 40)
    print()
    
    basic_string_conversion()
    link_and_image_control()
    boilerplate_removal()
    file_processing()
    language_specific_processing()
    
    print("✅ All examples completed!")
    print("\\nTry running the CLI as well:")
    print("  python -m html2cleantext.cli test_example.html")
    print("  python -m html2cleantext.cli test_example.html --mode text --no-links")
