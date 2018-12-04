# -*- coding: utf-8 -*-
import scrapy


class BaidutiebaSpider(scrapy.Spider):
    name = 'baiduTieba'
    allowed_domains = ['tieba.baidu.com']
    start_urls = ['http://tieba.baidu.com/']

    def parse(self, response):
        pass
