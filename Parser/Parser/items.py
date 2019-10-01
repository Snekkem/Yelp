# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ParserItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    product_link = scrapy.Field()
    product_title = scrapy.Field()
    address = scrapy.Field()
    product_phone = scrapy.Field()
    website = scrapy.Field()
    timetable = scrapy.Field()
    product_reviews = scrapy.Field()
    product_about = scrapy.Field()
    pass
