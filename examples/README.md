# html2cleantext Examples

This directory contains example scripts demonstrating various ways to use the html2cleantext package.

## Example Scripts

### 1. `basic_usage.py`
Demonstrates the core functionality of the package:
- Converting HTML strings to Markdown and text
- Controlling link and image preservation
- Boilerplate removal features
- File processing
- Language-specific normalization

```bash
python examples/basic_usage.py
```

### 2. `batch_processing.py`
Shows how to process multiple HTML files in batch:
- Processing entire directories of HTML files
- Saving output to organized directories
- Error handling for batch operations

```bash
python examples/batch_processing.py
```

### 3. `cli_examples.py`
Demonstrates various CLI usage patterns:
- All major command-line options
- Different output formats
- File input/output operations
- Error handling examples

```bash
python examples/cli_examples.py
```

## Quick CLI Examples

### Basic Usage
```bash
# Convert HTML file to Markdown
python -m html2cleantext.cli input.html

# Convert to plain text
python -m html2cleantext.cli input.html --mode text

# Save output to file
python -m html2cleantext.cli input.html --output clean.md
```

### Content Control
```bash
# Remove links and images
python -m html2cleantext.cli input.html --no-links --no-images

# Keep all content (no boilerplate removal)
python -m html2cleantext.cli input.html --no-strip-boilerplate

# Process with specific language
python -m html2cleantext.cli bengali.html --language bn
```

### Processing Different Sources
```bash
# Process HTML file
python -m html2cleantext.cli document.html

# Process raw HTML string
python -m html2cleantext.cli "<h1>Title</h1><p>Content</p>"

# Process URL (if supported in your environment)
python -m html2cleantext.cli "https://example.com/article"
```

## Python API Examples

### Basic Usage
```python
import html2cleantext

# Convert HTML string
html = "<h1>Title</h1><p>Content with <a href='#'>link</a></p>"
markdown = html2cleantext.to_markdown(html)
text = html2cleantext.to_text(html)

# Process file
markdown = html2cleantext.to_markdown("document.html")

# Process with options
clean_text = html2cleantext.to_text(
    html,
    keep_links=False,
    keep_images=False,
    remove_boilerplate=True,
    language='en'
)
```

### Advanced Usage
```python
# Batch processing
import glob

for html_file in glob.glob("*.html"):
    markdown_file = html_file.replace('.html', '.md')
    with open(markdown_file, 'w', encoding='utf-8') as f:
        f.write(html2cleantext.to_markdown(html_file))

# Language-specific processing
bengali_html = "<p>বাংলা টেক্সট</p>"
clean_bengali = html2cleantext.to_text(bengali_html, language='bn')

# URL processing (with error handling)
try:
    web_content = html2cleantext.to_markdown("https://example.com")
except Exception as e:
    print(f"Failed to process URL: {e}")
```

## Tips

1. **For best results with boilerplate removal**: Use the default settings on well-structured HTML documents.

2. **For preserving all content**: Use `remove_boilerplate=False` when you need to keep navigation, footers, etc.

3. **For clean text extraction**: Use `to_text()` with `keep_links=False` and `keep_images=False`.

4. **For multiple files**: Use the batch processing pattern shown in `batch_processing.py`.

5. **For non-English content**: Specify the language code for better normalization results.

## Running the Examples

Make sure you have html2cleantext installed:
```bash
pip install -e .  # If running from source
# or
pip install html2cleantext  # If installed from PyPI
```

Then run any of the example scripts:
```bash
python examples/basic_usage.py
python examples/batch_processing.py
python examples/cli_examples.py
```
