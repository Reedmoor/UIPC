#!/usr/bin/env python
"""
Main entry point for DNS scraper. 
This is a wrapper for backward compatibility with the original DNS parser.
"""
import os
import sys
import logging
from run import run_spider

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('dns_scraper.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

def main():
    """Main entry point for the DNS scraper."""
    # Get parameters from environment variables
    category = os.environ.get('CATEGORY', None)
    max_items = os.environ.get('MAX_ITEMS', 50)
    
    try:
        if max_items:
            max_items = int(max_items)
    except ValueError:
        logging.warning(f"Invalid MAX_ITEMS value: {max_items}. Using default: 50")
        max_items = 50
    
    # Run the spider
    success = run_spider(category, max_items)
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main() 