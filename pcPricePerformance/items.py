# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class ulItem(scrapy.Item):
    model = scrapy.Field()
    msrp = scrapy.Field()
    performance = scrapy.Field()
    popularity = scrapy.Field()