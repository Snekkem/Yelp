# -*- coding: utf-8 -*-
import scrapy
from ..items import ParserItem


class ParseSpiderSpider(scrapy.Spider):
    name = 'parse_spider'
    start_urls = ['https://www.yelp.com/search?find_desc=Restaurants&find_loc=LA']

    def parse(self, response):
        items = ParserItem()
        links = response.css('.text-color--black-regular__373c0__38bRH .link-size--inherit__373c0__2JXk5').css('::attr(href)').extract()

        title = response.css('.heading--inline__373c0__1F-Z6').css('::text').extract()
        address = response.css('.island-section__373c0__3vKXy .text-align--left__373c0__2pnx_ .lemon--span__373c0__3997G').css('::text').extract()
        phone = response.css('.text--offscreen__373c0__1SeFX+ .text-align--left__373c0__2pnx_').css('::text').extract()
        website = response.css('.text--offscreen__373c0__1SeFX+ .link-size--default__373c0__1skgq').css('::text').extract()
        timetable = response.css('.table-row__373c0__3wipe :nth-child(1) .text-align--left__373c0__2pnx_').css('::text').extract()
        reviews = response.css('.text-color--mid__373c0__3G312.text-size--large__373c0__1568g').css('::text').extract()
        items['title'] = title
        items['address'] = address
        items['phone'] = phone
        items['website'] = website
        items['timetable'] = timetable
        items['reviews'] = reviews

        items['links'] = links



        yield items
