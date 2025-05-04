"""
Spider for scraping products from DNS website.
"""
import json
import re
import os
from datetime import datetime

import scrapy
from scrapy.exceptions import CloseSpider
from ..items import ProductItem


class DnsProductsSpider(scrapy.Spider):
    name = "dns_products"
    allowed_domains = ["dns-shop.ru"]
    
    def __init__(self, category=None, max_items=None, *args, **kwargs):
        super(DnsProductsSpider, self).__init__(*args, **kwargs)
        self.start_urls = []
        self.max_items = int(max_items) if max_items else None
        self.items_count = 0
        
        # Load categories from JSON file
        try:
            # Get the directory of the current file
            current_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            categories_path = os.path.join(current_dir, 'categories.json')
            
            with open(categories_path, 'r', encoding='utf-8') as f:
                self.categories_list = json.load(f)
                
            # Convert list to dictionary for easier access
            self.categories = {}
            for cat in self.categories_list:
                self.categories[cat['name'].lower()] = cat['url']
                # Also add ID as possible key
                self.categories[cat['id']] = cat['url']
                
        except FileNotFoundError:
            self.logger.error("Categories file not found. Using defaults.")
            self.categories = {
                "videokarty": "https://www.dns-shop.ru/catalog/17a89aab16404e77/videokarty/",
                "processory": "https://www.dns-shop.ru/catalog/17a899cd16404e77/processory/",
                "materinskie-platy": "https://www.dns-shop.ru/catalog/17a89a0416404e77/materinskie-platy/"
            }
        
        # Set start URLs based on category
        if category:
            category = category.lower()
            if category in self.categories:
                self.start_urls = [self.categories[category]]
            else:
                self.logger.warning(f"Category '{category}' not found. Using all categories.")
                self.start_urls = list(self.categories.values())
        else:
            self.start_urls = list(self.categories.values())
    
    def parse(self, response):
        # Extract category name from URL
        category_match = re.search(r'/catalog/[^/]+/([^/]+)/', response.url)
        category = category_match.group(1) if category_match else "unknown"
        
        # Extract product links from page
        product_links = response.css('a.catalog-product__name::attr(href)').getall()
        
        for link in product_links:
            # Check if we've reached max items
            if self.max_items and self.items_count >= self.max_items:
                raise CloseSpider(f"Reached maximum number of items: {self.max_items}")
            
            self.items_count += 1
            yield response.follow(link, self.parse_product, meta={'category': category})
        
        # Follow pagination
        next_page = response.css('a.pagination-widget__page-link_next::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)
    
    def parse_product(self, response):
        item = ProductItem()
        
        # Basic product info
        item['name'] = response.css('h1.product-card-top__title::text').get()
        item['url'] = response.url
        
        # Extract product ID from URL
        product_id_match = re.search(r'/product/([^/]+)/', response.url)
        item['product_id'] = product_id_match.group(1) if product_id_match else None
        
        item['category'] = response.meta.get('category', 'unknown')
        
        # Price information
        price_original = response.css('div.product-buy__price-wrap span.product-buy__price::text').get()
        if price_original:
            item['price_original'] = price_original.strip().replace(' ', '')
        
        price_discounted = response.css('div.product-buy__price-wrap span.product-buy__price_active::text').get()
        if price_discounted:
            item['price_discounted'] = price_discounted.strip().replace(' ', '')
        
        # Availability
        available = response.css('div.product-buy__product-status button.button-ui_passive').get() is None
        item['availability'] = "In stock" if available else "Out of stock"
        
        # Rating and reviews
        item['rating'] = response.css('div.product-card-top__rating span.rating-stars::attr(data-rating)').get()
        review_count = response.css('div.product-card-top__rating span.product-card-top__rating-count::text').get()
        if review_count:
            item['review_count'] = review_count.strip('()').replace(' ', '')
        
        # Image URL
        item['image_url'] = response.css('div.product-images-slider img::attr(src)').get()
        
        # Brand
        item['brand'] = response.css('div.product-card-top__brand-logo img::attr(alt)').get()
        
        # Specifications - extract from structured data
        specs = {}
        spec_groups = response.css('div.product-characteristics__group')
        for group in spec_groups:
            group_name = group.css('div.product-characteristics__group-title::text').get('').strip()
            spec_items = {}
            for spec in group.css('div.product-characteristics__spec'):
                spec_name = spec.css('div.product-characteristics__spec-title::text').get('').strip()
                spec_value = spec.css('div.product-characteristics__spec-value::text').get('').strip()
                spec_items[spec_name] = spec_value
            specs[group_name] = spec_items
        
        item['specifications'] = specs
        
        # Description - could be in different sections, try to find main one
        description = response.css('div.product-card-description-text::text').getall()
        if description:
            item['description'] = ' '.join([desc.strip() for desc in description])
        
        # Timestamp of scraping
        item['date_scraped'] = datetime.now().isoformat()
        
        yield item 