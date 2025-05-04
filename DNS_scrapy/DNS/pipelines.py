# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


import json
import os
from itemadapter import ItemAdapter


class JsonWriterPipeline:
    """Pipeline for writing items to a JSON file."""
    
    def __init__(self):
        self.items = []
        
    def process_item(self, item, spider):
        """Process each item and add it to the items list."""
        self.items.append(ItemAdapter(item).asdict())
        return item
    
    def close_spider(self, spider):
        """When the spider is closed, write all items to a JSON file."""
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(os.path.abspath('items.json')), exist_ok=True)
        
        with open('items.json', 'w', encoding='utf-8') as f:
            json.dump(self.items, f, ensure_ascii=False, indent=4)
            
        spider.logger.info(f"Saved {len(self.items)} items to items.json")


class DnsPipeline:
    """Pipeline for processing and validating DNS items."""
    
    def __init__(self):
        self.ids_seen = set()
        
    def process_item(self, item, spider):
        """Process each item, check required fields and handle duplicates."""
        adapter = ItemAdapter(item)
        
        # Check for required fields
        if not adapter.get('product_id'):
            spider.logger.warning('Missing product_id in item, skipping')
            return None
            
        # Check for duplicates
        if adapter['product_id'] in self.ids_seen:
            spider.logger.debug(f"Duplicate item found: {adapter['product_id']}")
            return None
        else:
            self.ids_seen.add(adapter['product_id'])
            
        # Clean price fields if they exist
        if adapter.get('price_original'):
            adapter['price_original'] = adapter['price_original'].replace('\xa0', '').replace(' ', '')
            
        if adapter.get('price_discounted'):
            adapter['price_discounted'] = adapter['price_discounted'].replace('\xa0', '').replace(' ', '')
            
        return item 