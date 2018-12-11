# -*- coding: utf-8 -*-
import scrapy
import time
from scrapy.http import Request
from ..items import TiebaItems
from bs4 import BeautifulSoup
import requests
import datetime
from w3lib.html import remove_tags
import redis
key=redis.Redis(host="10.25.116.62",port=6379,max_connections=1000)
try:
    keywords = [key.get('newkeywords1').decode()]
except Exception:
    keywords = []
key_word_redislist=key.lrange('exists_keywords',0,-1)
key_word_list=[]
key_list=[]
for i in key_word_redislist:
    if i.decode() == '':
        continue
    if i.decode().strip() not in key_word_list:
        key_word_list.append(i.decode().strip())
for i in key_word_list:
    key_list+=i.split(' ')
key_list=set(key_list)
key_list=list(key_list)
key_list.remove('')

class TiebaSpider(scrapy.Spider):
    name = 'tieba'
    allowed_domains = ['tieba.baidu.com']
    start_urls = ['http://tieba.baidu.com/']
    if len(keywords)>0:
        key_words = keywords
    else:
        key_words =key_list
    page_url = []
    article_url = []

    def start_requests(self):
        print('开始')
        print(self.key_words)
        for key_word in self.key_words:
            urls = ['http://tieba.baidu.com/f/search/res?ie=utf-8&qw=%s']
            # meta = {'proxy': 'http://211.138.61.27'}
            for url in urls:
                yield Request(url=url % key_word)

    def parse(self, response):
        print('解析')
        # 直接获取当前页面下的所有分页
        n = response.css('.pager-search')
        page_list = n.xpath('./a')
        start_href = n.xpath('./a[1]/@href').extract_first()
        num = start_href.rindex('=')
        self.page_url.append(start_href[0:num + 1] + '1')
        for i in page_list:
            if (not i.xpath('./text()').extract_first() in ['首页', '尾页', '下一页>', '<上一页']) and (
                    not i.xpath('./@href').extract_first() in self.page_url):
                self.page_url.append(i.xpath('./@href').extract_first())
        for i in self.page_url:
            yield Request(url='http://tieba.baidu.com' + i, callback=self.storage)

    def storage(self, response):
        print('存储')
        # print(response.url)
        print(response)
        list = response.css('.s_post')
        for i in list:
            try:
                article_title = remove_tags(i.xpath('.//span/a').extract_first(), 'a')
            except Exception:
                article_title = '回复'
            # 判断内容不是一个回复且不是一个贴吧名字
            if article_title[0:2] != '回复' and not i.xpath('.//p'):
                article_url = 'http://tieba.baidu.com' + i.xpath('.//span/a/@href').extract_first()
                article_detail = i.xpath('.//div/text()').extract_first()
                if not article_detail:
                    article_detail='无文章简介'
                author = i.xpath('.//a[2]/font/text()').extract_first()
                if not author:
                    author = '无作者'
                author_url = 'http://tieba.baidu.com' + i.xpath('.//a[2]/@href').extract_first()
                create_time = i.xpath('./font/text()').extract_first()
                create_time = datetime.datetime.strptime(create_time, '%Y-%m-%d %H:%M')
                m = self.articledetail(article_url)
                article_type = m[2]
                content = m[0]
                affected_count = m[1]
                # print(response.text)
                keyword=response.css('.tb_header_search_input').xpath('./@value').extract_first()
                print(keyword)
                yield TiebaItems(
                    author=author,
                    author_url=author_url,
                    article_title=article_title,
                    article_content=content,
                    article_detail=article_detail,
                    article_url=article_url,
                    article_create_time=create_time,
                    article_from='百度贴吧',
                    affected_count=affected_count,
                    article_type=article_type,
                    keyword=keyword,
                )

    # 获取文章详情和影响人数,文章类型
    def articledetail(self, url):
        response = requests.get(url=url)
        html = response.text
        soup = BeautifulSoup(html, 'lxml')
        try:
            content = soup.find_all(attrs={'class': 'd_post_content'})[0]
        except Exception:
            content = '文章为空'
        if soup.find_all('title')[0].text[0:4] == '【图片】':
            article_type = 'img'
        elif soup.find_all('title')[0].text[0:4] == '【视频】':
            article_type = 'video'
            video_src = content.find_all(attrs={'class': 'BDE_Flash'})[0].attrs['data-video']
            video_html = '''<video controls>
                    <source src="%s" type="video/mp4">
                        您的浏览器不支持 video 标签。
                  </video>''' % video_src

            content = video_html
        else:
            article_type = 'text'
        affected_count_html = soup.find_all(attrs={'class': 'l_reply_num'})[0]
        affected_soup = BeautifulSoup(html, 'lxml')
        affected_count = affected_soup.find_all(attrs={'style': 'margin-right:3px'})[0].text
        return str(content), int(affected_count), article_type
