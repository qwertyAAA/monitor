# -*- coding: utf-8 -*-
import scrapy
import time
from scrapy.http import Request
from ..items import TiebaItems
from bs4 import BeautifulSoup
import requests
import datetime
from w3lib.html import remove_tags
from ..startTieba import tieba


class TiebaSpider(scrapy.Spider):
    name = 'tieba'
    allowed_domains = ['tieba.baidu.com']
    start_urls = ['http://tieba.baidu.com/']
    key_words = ['大庆油田']
    # key_words = tieba.get_keywords()
    page_url = []
    article_url = []

    def start_requests(self):
        print('开始')
        for key_word in self.key_words:
            urls = ['http://tieba.baidu.com/f/search/res?ie=utf-8&qw=%s']
            # meta = {'proxy': 'http://211.138.61.27'}
            for url in urls:
                yield Request(url=url % key_word)

    def parse(self, response):
        print('解析')
        # print(response.text)
        # self.page_url.append('http://tieba.baidu.com/f/search/res?isnew=1&kw=&qw=%B4%F3%C7%EC%D3%CD%CC%EF&rn=10&un=&only_thread=0&sm=1&sd=&ed=&pn=1')
        # 通过获取尾页url来获取全部url
        # end_href=brower.find_element_by_xpath('/html/body/div[4]/div/div[2]/div[5]/a[11]').get_attribute('href')
        # num=end_href.rindex('=')
        # end_page=end_href[num+1:]
        # print(end_page)
        # page_list = brower.find_elements_by_xpath('/html/body/div[4]/div/div[2]/div[5]/a')
        # for i in range(1,int(end_page)+1):
        #     yield Request(url=end_href[0:num+1]+str(i), callback=self.index)
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
        print(response.url)
        print()
        list = response.css('.s_post')
        for i in list:
            print('***********************************************************')
            try:
                article_title = remove_tags(i.xpath('.//span/a').extract_first(), 'a')
            except Exception:
                article_title = '回复'
            # 判断内容不是一个回复且不是一个贴吧名字
            if article_title[0:2] != '回复' and not i.xpath('.//p'):
                article_url = 'http://tieba.baidu.com' + i.xpath('.//span/a/@href').extract_first()
                article_detail = i.xpath('.//div/text()').extract_first()
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
                # yield Request(response.url,callback=self.parse)
                # title=item["article"],
                # content=item["article"],
                # author = scrapy.Field()
                # author_url = scrapy.Field()
                # article = scrapy.Field()
                # article_url = scrapy.Field()
                # article_create_time = scrapy.Field()
                # article_from = scrapy.Field()
                # affected_count = scrapy.Field()
                print(article_url, article_title, affected_count)
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
                    article_type=article_type
                )

    # 获取文章详情和影响人数,文章类型
    def articledetail(self, url):
        response = requests.get(url=url)
        html = response.text
        soup = BeautifulSoup(html, 'lxml')
        content = soup.find_all(attrs={'class': 'd_post_content'})[0]
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
