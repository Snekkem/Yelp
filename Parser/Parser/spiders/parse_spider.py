# -*- coding: utf-8 -*-
import re
import time

import scrapy

from ..items import ParserItem


class ParseSpiderSpider(scrapy.Spider):
    name = 'parse_spider'
    page_number = 0
    start_urls = ['https://www.yelp.com/search?find_desc=Restaurants&find_loc=LA&ns=1',
                  'https://www.yelp.com/search?find_desc=Restaurants&find_loc=NY',
                  'https://www.yelp.com/search?find_desc=Restaurants&find_loc=SF',
                  'https://www.yelp.com/search?find_desc=Gyms&find_loc=SF',
                  'https://www.yelp.com/search?find_desc=Gyms&find_loc=NY',
                  'https://www.yelp.com/search?find_desc=Gyms&find_loc=LA',
                  'https://www.yelp.com/search?find_desc=Spa&find_loc=LA',
                  'https://www.yelp.com/search?find_desc=Spa&find_loc=NY',
                  'https://www.yelp.com/search?find_desc=Spa&find_loc=SF']

    def parse(self, response):
        # The main method of the spider. It scrapes the URL(s) specified in the
        # 'start_url' argument above. The content of the scraped URL is passed on
        # as the 'response' object.

        # nextpageurl = '' #response.css('.u-space-l2 .text-align--left__373c0__2pnx_').css('::attr(href)').extract()

        # f = open('text.txt', 'a')
        # print(response.text)
        for item in self.scrape(response):
            time.sleep(1)
            yield item

        next_page = 'https://www.yelp.com/search?find_desc=Restaurants&find_loc=LA&ns=1&start=' + str(ParseSpiderSpider.page_number) + ''
        if ParseSpiderSpider.page_number is not None:
            ParseSpiderSpider.page_number += 30
            yield response.follow(next_page, callback=self.parse)

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

        item['rest_title'] = response.css('.heading--inline__373c0__1F-Z6').css('::text').extract_first()
        item['rest_phone'] = response.css('.text--offscreen__373c0__1SeFX+ .text-align--left__373c0__2pnx_').css(
            '::text').extract_first()
        item['rest_reviews'] = response.css('.text-color--mid__373c0__3G312.text-size--large__373c0__1568g').css(
             '::text').extract_first()
        item['rest_address'] = response.css('.island-section__373c0__3vKXy .text-align--left__373c0__2pnx_ '
                                            '.lemon--span__373c0__3997G').css('::text').extract()
        item['rest_timetable'] = response.css('.table-row__373c0__3wipe :nth-child(1) .text-align--left__373c0__2pnx_').css(
              '::text').extract()

        item['rest_link'] = response.css('.text--offscreen__373c0__1SeFX+ .link-size--default__373c0__1skgq').css(
             '::text').extract_first()

        about = response.xpath(
            '//p[@class="lemon--p__373c0__3Qnnj text__373c0__2pB8f text-color--normal__373c0__K_MKN text-align--left__373c0__2pnx_"]')
        about = about.xpath('//span[@width="0"]').xpath("/span").extract_first()
        item['rest_about'] = about

        item['gym_title'] = response.css('.biz-page-title').css('::text').extract_first()

        rev = response.css('.biz-rating-very-large .rating-qualifier').css('::text').extract_first()
        rev = re.sub(r'(\\\\r|\\\\n|\\\\r\\\\n)*\s\s+', "", str(rev)).strip()
        item['gym_reviews'] = rev


        some = response.xpath('//*[@id="wrap"]/div[2]/div/div[1]/div/div[4]/div[1]/div/div[2]/ul/li[1]/div/strong/address/text()').extract()
        some = re.sub(r'(\\\\r|\\\\n|\\\\r\\\\n|\\n|\\r)?|\s\s+', "", str(some)).strip()
        item['gym_address'] = some

        phone = response.css('.biz-phone').css('::text').extract_first()
        phone = re.sub(r'(\\\\r|\\\\n|\\\\r\\\\n)*\s\s+', "", str(phone)).strip()
        item['gym_phone'] = phone
        item['gym_link'] = response.css('.js-add-url-tagging a').css('::text').extract_first()
        table = response.xpath('//table[@class="table table-simple hours-table"]')

        times = table.xpath('//span[@class="nowrap"]/text()').extract()
        days = table.xpath('//th[@scope="row"]/text()').getall()

        listData = []
        temp = []
        result = []

        try:
            for el in range(5, 12):
                listData.append(days[el])

            for el in range(2, 16, 2):
                temp.append(times[el] + ' ' + times[el + 1])

            for el in range(7):
                result.append(listData[el] + ' ' + temp[el])
        except IndexError:
            print('s')

        item['gym_timetable'] = result

        item['gym_link_img'] = response.css('.photo-2 .photo-box-img').css('::attr(src)').extract_first()

        yield item  # Return the new phonenumber'd item back to scrape
    # scrapy crawl parse_spider
