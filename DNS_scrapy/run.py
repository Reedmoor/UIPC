#!/usr/bin/env python
import os
import subprocess
import sys
import logging
import json

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('dns_scraper.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

def run_spider(category=None, max_items=50):
    """Run the DNS spider with the given parameters."""
    try:
        # Get the current directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Set up command
        spider_name = 'dns_products'
        cmd = ['scrapy', 'crawl', spider_name]
        
        # Add parameters if provided
        if category:
            cmd.extend(['-a', f'category={category}'])
        if max_items:
            cmd.extend(['-a', f'max_items={max_items}'])
            
        # Set the working directory to the project root
        os.chdir(current_dir)
        
        # Run the spider
        logging.info(f"Running command: {' '.join(cmd)}")
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        
        # Stream output to the console
        for line in process.stdout:
            line = line.strip()
            print(line)
            
        # Wait for the process to complete
        process.wait()
        
        # Check if the process completed successfully
        if process.returncode != 0:
            stderr_output = process.stderr.read()
            logging.error(f"Spider failed with return code {process.returncode}")
            logging.error(stderr_output)
            return False
            
        # Check if items.json was created
        items_file = os.path.join(current_dir, 'items.json')
        if not os.path.exists(items_file):
            logging.error(f"No items.json file created at {items_file}")
            return False
            
        # Read items.json to report success
        with open(items_file, 'r', encoding='utf-8') as f:
            items = json.load(f)
            
        logging.info(f"Spider completed successfully. Scraped {len(items)} items.")
        return True
    
    except Exception as e:
        logging.error(f"Error running DNS spider: {str(e)}")
        return False

if __name__ == "__main__":
    # Parse command line arguments
    category = None
    max_items = 50
    
    if len(sys.argv) > 1:
        category = sys.argv[1]
    if len(sys.argv) > 2:
        try:
            max_items = int(sys.argv[2])
        except ValueError:
            logging.warning(f"Invalid max_items value: {sys.argv[2]}. Using default: 50")
    
    # Get category from environment variable if not provided as argument
    if not category and 'CATEGORY' in os.environ:
        category = os.environ['CATEGORY']
        
    # Get max_items from environment variable if not provided as argument
    if 'MAX_ITEMS' in os.environ:
        try:
            max_items = int(os.environ['MAX_ITEMS'])
        except ValueError:
            logging.warning(f"Invalid MAX_ITEMS environment variable: {os.environ['MAX_ITEMS']}. Using: {max_items}")
    
    # Run the spider
    success = run_spider(category, max_items)
    
    # Exit with appropriate code
    sys.exit(0 if success else 1) 