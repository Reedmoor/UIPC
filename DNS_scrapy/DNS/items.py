# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ProductItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    url = scrapy.Field()
    product_id = scrapy.Field()
    category = scrapy.Field()
    price_original = scrapy.Field()
    price_discounted = scrapy.Field()
    availability = scrapy.Field()
    rating = scrapy.Field()
    review_count = scrapy.Field()
    image_url = scrapy.Field()
    brand = scrapy.Field()
    specifications = scrapy.Field()
    description = scrapy.Field()
    date_scraped = scrapy.Field() 