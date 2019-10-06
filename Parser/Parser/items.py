# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ParserItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    # Restaurants
    rest_link = scrapy.Field()
    rest_title = scrapy.Field()
    rest_address = scrapy.Field()
    rest_phone = scrapy.Field()
    rest_timetable = scrapy.Field()
    rest_reviews = scrapy.Field()
    rest_about = scrapy.Field()
    rest_link_img = scrapy.Field()
    rest_email = scrapy.Field()

    gym_link = scrapy.Field()
    gym_title = scrapy.Field()
    gym_address = scrapy.Field()
    gym_phone = scrapy.Field()
    gym_timetable = scrapy.Field()
    gym_reviews = scrapy.Field()
    gym_about = scrapy.Field()
    gym_link_img = scrapy.Field()
    gym_email = scrapy.Field()

    next_page = scrapy.Field()
    pass
