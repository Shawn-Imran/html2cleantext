#!/usr/bin/env python3
"""
Batch processing example for html2cleantext.

This script demonstrates how to process multiple HTML files in batch.
"""

import html2cleantext
import os
import glob
from pathlib import Path


def process_html_files_in_directory(input_dir: str, output_dir: str, mode: str = 'markdown'):
    """
    Process all HTML files in a directory and save the results.
    
    Args:
        input_dir: Directory containing HTML files
        output_dir: Directory to save converted files
        mode: Output mode ('markdown' or 'text')
    """
    # Create output directory if it doesn't exist
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # Find all HTML files
    html_files = glob.glob(os.path.join(input_dir, "*.html")) + \
                 glob.glob(os.path.join(input_dir, "*.htm"))
    
    if not html_files:
        print(f"No HTML files found in {input_dir}")
        return
    
    print(f"Found {len(html_files)} HTML files to process")
    
    for html_file in html_files:
        try:
            # Determine output filename
            base_name = Path(html_file).stem
            if mode == 'markdown':
                output_file = os.path.join(output_dir, f"{base_name}.md")
                result = html2cleantext.to_markdown(html_file)
            else:
                output_file = os.path.join(output_dir, f"{base_name}.txt")
                result = html2cleantext.to_text(html_file)
            
            # Save the result
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(result)
            
            print(f"✅ Processed: {html_file} -> {output_file}")
            
        except Exception as e:
            print(f"❌ Error processing {html_file}: {e}")


def create_sample_files():
    """Create some sample HTML files for demonstration."""
    sample_files = {
        'article1.html': """
        <html>
        <head><title>Article 1</title></head>
        <body>
            <nav>Navigation</nav>
            <article>
                <h1>First Article</h1>
                <p>This is the content of the first article.</p>
                <p>It has multiple paragraphs and <a href="#">links</a>.</p>
            </article>
            <footer>Footer</footer>
        </body>
        </html>
        """,
        
        'article2.html': """
        <html>
        <head><title>Article 2</title></head>
        <body>
            <header>Site Header</header>
            <main>
                <h1>Second Article</h1>
                <p>This is a different article with <strong>emphasis</strong>.</p>
                <ul>
                    <li>Item A</li>
                    <li>Item B</li>
                </ul>
            </main>
            <aside>Sidebar content</aside>
        </body>
        </html>
        """,
        
        'page3.html': """
        <html>
        <body>
            <h2>Simple Page</h2>
            <p>Just a simple page with minimal content.</p>
            <img src="image.jpg" alt="Sample image">
        </body>
        </html>
        """
    }
    
    # Create sample_input directory
    input_dir = "sample_input"
    Path(input_dir).mkdir(exist_ok=True)
    
    for filename, content in sample_files.items():
        filepath = os.path.join(input_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Created sample file: {filepath}")
    
    return input_dir


def main():
    """Main function demonstrating batch processing."""
    print("html2cleantext - Batch Processing Example")
    print("=" * 45)
    print()
    
    # Create sample files
    print("Creating sample HTML files...")
    input_dir = create_sample_files()
    print()
    
    # Process to Markdown
    print("Processing to Markdown...")
    process_html_files_in_directory(input_dir, "output_markdown", mode='markdown')
    print()
    
    # Process to Text
    print("Processing to Text...")
    process_html_files_in_directory(input_dir, "output_text", mode='text')
    print()
    
    print("✅ Batch processing completed!")
    print(f"\\nCheck the output directories:")
    print(f"  - output_markdown/ (Markdown files)")
    print(f"  - output_text/ (Text files)")
    
    # Clean up sample files
    print("\\nCleaning up sample files...")
    import shutil
    if os.path.exists(input_dir):
        shutil.rmtree(input_dir)
        print(f"Removed {input_dir}")


if __name__ == "__main__":
    main()
