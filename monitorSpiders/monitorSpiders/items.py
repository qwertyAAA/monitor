# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WeiboItems(scrapy.Item):
    keyword = scrapy.Field()
    author = scrapy.Field()
    author_url = scrapy.Field()
    article_title = scrapy.Field()
    article_content = scrapy.Field()
    article_detail = scrapy.Field()
    article_url = scrapy.Field()
    article_type = scrapy.Field()
    article_create_time = scrapy.Field()
    affected_count = scrapy.Field()


class TiebaItems(scrapy.Item):
    author = scrapy.Field()
    author_url = scrapy.Field()
    article_title = scrapy.Field()
    article_content = scrapy.Field()
    article_url = scrapy.Field()
    article_detail = scrapy.Field()
    article_create_time = scrapy.Field()
    article_from = scrapy.Field()
    affected_count = scrapy.Field()
    article_type = scrapy.Field()
