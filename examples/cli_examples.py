#!/usr/bin/env python3
"""
CLI usage examples for html2cleantext.

This script demonstrates various command-line interface usage patterns.
Run this script to see example CLI commands and their outputs.
"""

import subprocess
import tempfile
import os
from pathlib import Path


def run_cli_command(command: list, description: str):
    """Run a CLI command and display the result."""
    print(f"=== {description} ===")
    print(f"Command: {' '.join(command)}")
    print("Output:")
    
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        print(result.stdout)
        if result.stderr:
            print(f"Warnings: {result.stderr}")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        if e.stderr:
            print(f"Error details: {e.stderr}")
    
    print("-" * 50)
    print()


def create_sample_file():
    """Create a sample HTML file for CLI demonstrations."""
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <title>Sample Article</title>
        <style>body { font-family: Arial; }</style>
    </head>
    <body>
        <nav>
            <a href="/">Home</a> | <a href="/about">About</a>
        </nav>
        
        <main>
            <h1>How to Use html2cleantext</h1>
            <p>This is a comprehensive guide to using the <strong>html2cleantext</strong> package.</p>
            
            <h2>Key Features</h2>
            <ul>
                <li>Convert HTML to Markdown</li>
                <li>Extract plain text</li>
                <li>Remove boilerplate content</li>
                <li>Support multiple languages</li>
            </ul>
            
            <p>For more information, visit our <a href="https://github.com/example/html2cleantext">GitHub repository</a>.</p>
            
            <img src="demo.png" alt="Demo screenshot">
            
            <blockquote>
                "This tool has revolutionized how we process HTML content." - Happy User
            </blockquote>
        </main>
        
        <footer>
            <p>&copy; 2025 Example Company</p>
            <div class="social">
                <a href="/twitter">Twitter</a> | <a href="/facebook">Facebook</a>
            </div>
        </footer>
        
        <script>
            console.log("This script will be removed");
        </script>
    </body>
    </html>
    """
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as f:
        f.write(html_content)
        return f.name


def demonstrate_cli_usage():
    """Demonstrate various CLI usage patterns."""
    print("html2cleantext - CLI Usage Examples")
    print("=" * 40)
    print()
    
    # Create sample file
    sample_file = create_sample_file()
    print(f"Created sample file: {sample_file}")
    print()
    
    try:
        # Basic conversion (default: Markdown output)
        run_cli_command(
            ["python", "-m", "html2cleantext.cli", sample_file],
            "Basic Conversion (Default: Markdown)"
        )
        
        # Convert to plain text
        run_cli_command(
            ["python", "-m", "html2cleantext.cli", sample_file, "--mode", "text"],
            "Convert to Plain Text"
        )
        
        # Remove links and images
        run_cli_command(
            ["python", "-m", "html2cleantext.cli", sample_file, "--no-links", "--no-images"],
            "Remove Links and Images"
        )
        
        # Keep all content (no boilerplate removal)
        run_cli_command(
            ["python", "-m", "html2cleantext.cli", sample_file, "--no-strip-boilerplate"],
            "Keep All Content (No Boilerplate Removal)"
        )
        
        # Text mode with no links/images
        run_cli_command(
            ["python", "-m", "html2cleantext.cli", sample_file, "--mode", "text", "--no-links", "--no-images"],
            "Clean Text Mode"
        )
        
        # Save output to file
        output_file = "sample_output.md"
        run_cli_command(
            ["python", "-m", "html2cleantext.cli", sample_file, "--output", output_file],
            f"Save Output to File ({output_file})"
        )
        
        # Show the saved file content
        if os.path.exists(output_file):
            print("=== Saved File Content ===")
            with open(output_file, 'r', encoding='utf-8') as f:
                print(f.read())
            print("-" * 50)
            print()
            os.unlink(output_file)
        
        # Show version
        run_cli_command(
            ["python", "-m", "html2cleantext.cli", "--version"],
            "Show Version"
        )
        
        # Process raw HTML string
        html_string = "<h1>Direct HTML</h1><p>Processing HTML string directly.</p>"
        run_cli_command(
            ["python", "-m", "html2cleantext.cli", html_string],
            "Process Raw HTML String"
        )
        
    finally:
        # Clean up
        os.unlink(sample_file)
        print(f"Cleaned up sample file: {sample_file}")


def show_help():
    """Show the CLI help."""
    print("=== CLI Help ===")
    print("Command: python -m html2cleantext.cli --help")
    print("Output:")
    
    try:
        result = subprocess.run(
            ["python", "-m", "html2cleantext.cli", "--help"], 
            capture_output=True, text=True
        )
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error getting help: {e}")
    
    print("-" * 50)
    print()


if __name__ == "__main__":
    show_help()
    demonstrate_cli_usage()
    
    print("\\n🎉 CLI examples completed!")
    print("\\nTry these commands yourself:")
    print("  python -m html2cleantext.cli test_example.html")
    print("  python -m html2cleantext.cli test_example.html --mode text")
    print("  python -m html2cleantext.cli --help")
