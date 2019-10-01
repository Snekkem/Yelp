# -*- coding: utf-8 -*-
import scrapy
from ..items import ParserItem


class ParseSpiderSpider(scrapy.Spider):
    name = 'parse_spider'
    start_urls = ['https://www.yelp.com/search?find_desc=Restaurants&find_loc=LA']

    def parse(self, response):
        # The main method of the spider. It scrapes the URL(s) specified in the
        # 'start_url' argument above. The content of the scraped URL is passed on
        # as the 'response' object.

        # nextpageurl = '' #response.css('.u-space-l2 .text-align--left__373c0__2pnx_').css('::attr(href)').extract()

        f = open('text.txt', 'a')

        for item in self.scrape(response):
            yield item

        # if nextpageurl:
        #  path = nextpageurl.extract_first()
        # nextpage = response.urljoin(path)
        #  print("Found url: {}".format(nextpage))
        # yield scrapy.Request(nextpage, callback=self.parse)

    def scrape(self, response):
        for resource in response.css('.text-color--black-regular__373c0__38bRH .link-size--inherit__373c0__2JXk5'):
            # Loop over each item on the page.
            item = ParserItem()  # Creating a new Item object

            # item['name'] = resource.css('::text').extract_first()

            # Instead of just writing the relative path of the profile page, lets make the full profile page so we can use it later.
            # print(resource.css('::attr(href)').extract_first())
            profilepage = response.urljoin(resource.css('::attr(href)').extract_first())
            # item['link'] = profilepage

            # item['district'] = resource.xpath("dl/dd/text()").extract_first()
            # item['twitter'] = resource.xpath("dl/dd/a[contains(@class, 'twitter')]/@href").extract_first()
            # item['party'] = resource.xpath("dl/dt[text()='Party']/following-sibling::dd/text()").extract_first()

            # We need to make a new variable that the scraper will return that will get passed through another callback. We're calling that variable "request"
            request = scrapy.Request(profilepage, callback=self.get_phonenumber)
            request.meta['item'] = item  # By calling .meta, we can pass our item object into the callback.
            yield request  # Return the item + phonenumber back to the parser.

    def get_phonenumber(self, response):
        # A scraper designed to operate on one of the profile pages
        item = response.meta['item']  # Get the item we passed from scrape()
        item['product_title'] = response.css('.heading--inline__373c0__1F-Z6').css('::text').extract_first()
        item['product_phone'] = response.css('.text--offscreen__373c0__1SeFX+ .text-align--left__373c0__2pnx_').css(
            '::text').extract_first()
        item['product_reviews'] = response.css('.text-color--mid__373c0__3G312.text-size--large__373c0__1568g').css(
            '::text').extract_first()
        item['product_link'] = response.css('.text--offscreen__373c0__1SeFX+ .link-size--default__373c0__1skgq').css(
            '::text').extract_first()

        item1 = response.xpath('//p[@class="lemon--p__373c0__3Qnnj text__373c0__2pB8f text-color--normal__373c0__K_MKN text-align--left__373c0__2pnx_"]')
        item1 = item1.xpath('//span[@width="0"]/text()')
        print(item1)



        yield item  # Return the new phonenumber'd item back to scrape
