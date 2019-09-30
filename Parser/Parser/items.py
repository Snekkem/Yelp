# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ParserItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    links = scrapy.Field()
    title = scrapy.Field()
    address = scrapy.Field()
    phone = scrapy.Field()
    website = scrapy.Field()
    timetable = scrapy.Field()
    reviews = scrapy.Field()
    pass
