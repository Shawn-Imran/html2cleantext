"""
Command-line interface for html2cleantext.
"""

import argparse
import sys
import logging
from pathlib import Path
from typing import Optional

from . import __version__
from .core import to_markdown, to_text


def setup_logging(verbose: bool = False) -> None:
    """
    Set up logging configuration.
    
    Args:
        verbose: Whether to enable verbose (debug) logging
    """
    level = logging.DEBUG if verbose else logging.WARNING
    logging.basicConfig(
        level=level,
        format='%(levelname)s: %(message)s',
        stream=sys.stderr
    )


def main() -> None:
    """
    Main CLI entry point.
    """
    parser = argparse.ArgumentParser(
        description="Convert HTML to clean, structured Markdown or plain text",
        prog="html2cleantext"
    )
    
    # Version
    parser.add_argument(
        '--version', 
        action='version', 
        version=f'%(prog)s {__version__}'
    )
    
    # Input source
    parser.add_argument(
        'input',
        help='HTML input: file path, URL, or raw HTML string'
    )
    
    # Output mode
    parser.add_argument(
        '--mode', '-m',
        choices=['markdown', 'text'],
        default='markdown',
        help='Output format (default: markdown)'
    )
    
    # Output file
    parser.add_argument(
        '--output', '-o',
        type=str,
        help='Output file path (default: stdout)'
    )
    
    # Content options
    parser.add_argument(
        '--keep-links',
        action='store_true',
        help='Preserve links in the output (default for markdown mode)'
    )
    
    parser.add_argument(
        '--no-links',
        action='store_true',
        help='Remove links from the output (default for text mode)'
    )
    
    parser.add_argument(
        '--keep-images',
        action='store_true',
        help='Preserve images in the output (default for markdown mode)'
    )
    
    parser.add_argument(
        '--no-images',
        action='store_true',
        help='Remove images from the output (default for text mode)'
    )
    
    parser.add_argument(
        '--strip-boilerplate',
        action='store_true',
        default=True,
        help='Remove navigation, footers, and boilerplate content (default: enabled)'
    )
    
    parser.add_argument(
        '--no-strip-boilerplate',
        action='store_true',
        help='Keep all content including navigation and footers'
    )
    
    # Language options
    parser.add_argument(
        '--language', '-l',
        type=str,
        help='Language code for normalization (auto-detected if not specified)'
    )
    
    parser.add_argument(
        '--no-normalize',
        action='store_true',
        help='Skip language-specific normalization'
    )
    
    # Logging
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose logging'
    )
    
    args = parser.parse_args()
    
    # Set up logging
    setup_logging(args.verbose)
    
    try:
        # Determine link and image options based on mode and flags
        keep_links = _determine_keep_links(args)
        keep_images = _determine_keep_images(args)
        remove_boilerplate = not args.no_strip_boilerplate
        normalize_lang = not args.no_normalize
        
        # Convert HTML
        if args.mode == 'markdown':
            result = to_markdown(
                args.input,
                keep_links=keep_links,
                keep_images=keep_images,
                remove_boilerplate=remove_boilerplate,
                normalize_lang=normalize_lang,
                language=args.language
            )
        else:  # text mode
            result = to_text(
                args.input,
                keep_links=keep_links,
                keep_images=keep_images,
                remove_boilerplate=remove_boilerplate,
                normalize_lang=normalize_lang,
                language=args.language
            )
        
        # Output result
        if args.output:
            output_path = Path(args.output)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(result)
            print(f"Output written to: {output_path}", file=sys.stderr)
        else:
            print(result)
            
    except KeyboardInterrupt:
        print("\nOperation cancelled by user", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


def _determine_keep_links(args) -> bool:
    """
    Determine whether to keep links based on mode and flags.
    
    Args:
        args: Parsed command line arguments
        
    Returns:
        bool: Whether to keep links
    """
    if args.no_links:
        return False
    elif args.keep_links:
        return True
    else:
        # Default behavior: keep links in markdown mode, remove in text mode
        return args.mode == 'markdown'


def _determine_keep_images(args) -> bool:
    """
    Determine whether to keep images based on mode and flags.
    
    Args:
        args: Parsed command line arguments
        
    Returns:
        bool: Whether to keep images
    """
    if args.no_images:
        return False
    elif args.keep_images:
        return True
    else:
        # Default behavior: keep images in markdown mode, remove in text mode
        return args.mode == 'markdown'


if __name__ == '__main__':
    main()
