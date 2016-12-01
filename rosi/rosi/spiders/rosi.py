# -*- coding: utf-8 -*-

import scrapy
from scrapy.loader import ItemLoader 
from rosi.items import RosiItem
import re
class RosiSpider(scrapy.Spider):
    name = "rosi"
    allowed_domains = ['mmxyz.net']
    custom_settings = {
        "DOWNLOAD_TIMEOUT"      : 30,
        # "ITEM_PIPELINES"        :{'rosi.pipelines.RosiPipeline': 2},
    }
    start_urls = [
        'http://www.mmxyz.net/?action=ajax_post&pag=',
    ]

    def start_requests(self):
        for i in range(1,2):
            url = 'http://www.mmxyz.net/?action=ajax_post&pag=%s'%i
            yield scrapy.Request(url, callback=self.parse, errback=self.errback, dont_filter=True)

    def parse(self, response):
        print('url:',response.url)

        if re.search('/rosi\-\d+/$', response.url) :
            yield self.parse_item(response)
        for a in response.css('a::attr(href)').extract():
            if not a:
                continue
            if re.search('/rosi\-\d+/$', a):
                print(a)
                yield scrapy.Request(a, callback=self.parse)
    def parse_item(self, response):
        il = ItemLoader(item=RosiItem(), response=response)
        il.add_css('image_urls', 'img::attr(src)')
        return il.load_item()

    def errback(self, failure):
        pass

