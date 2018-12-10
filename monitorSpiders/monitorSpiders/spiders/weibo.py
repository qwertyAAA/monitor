# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from scrapy.selector import Selector
import re
import time
from ..items import WeiboItems
from urllib.parse import unquote
from w3lib.html import remove_tags


# 将微博的创建时间进行格式化
def get_time(time_str):
    time_str = re.sub(r"\D", " ", time_str)
    time_str = time_str.strip()
    if 5 < len(time_str) <= 12:
        time_str = time.strftime("%Y ") + time_str
        time_str = time.strftime("%Y-%m-%d %H:%M", time.strptime(time_str, "%Y %m %d %H %M"))
    elif 2 < len(time_str) <= 5:
        time_str = time.strftime("%Y-%m-%d ") + time_str.replace(" ", ":")
    elif 0 < len(time_str) <= 2:
        stamp = time.time() - float(time_str) * 60
        time_str = time.strftime("%Y-%m-%d %H:%M", time.localtime(stamp))
    else:
        time_str = time.strftime("%Y-%m-%d %H:%M")
    return time_str


# 获取点赞、评论、转发数
def get_count(common_str):
    if not isinstance(common_str, str):
        count = 0
        return count
    digit_str = re.sub(r"\D", "", common_str)
    if not digit_str:
        count = 0
    else:
        count = int(digit_str)
    return count


# 获取media文章关键字
def get_media_keyword(url):
    temp = url.split("/")[-1]
    keyword = unquote(temp.split("&")[0])
    return keyword


# 获取普通文章关键字
def get_normal_keyword(url):
    return unquote(url.split("=")[1].split("&")[0])


def handle_article_detail(prev_content):
    article_type = "text"
    videos = prev_content.xpath(".//video")
    videos_html = ""
    imgs = prev_content.xpath(".//img")
    imgs_html = ""
    p = prev_content.xpath("./div[@class='detail']//p")
    p_html = ""
    if p.extract_first():
        article_type = "text"
        p_html = p.extract_first()
    if imgs.extract():
        article_type = "img"
        for img in imgs:
            imgs_html += "<img src='{}'/>\n".format(img.xpath("./@src").extract_first())
    if videos.extract():
        article_type = "video"
        for video in videos:
            videos_html += "<video controls><source src='{}'></video>".format(video.xpath("./@src").extract_first())

    detail = "<div class='content'>" + p_html + imgs_html + videos_html + "</div>"
    return detail, article_type


class WeiboSpider(scrapy.Spider):
    name = 'weibo'
    allowed_domains = ['weibo.com']
    start_urls = [
        'https://s.weibo.com/weibo/{}',
        'https://s.weibo.com/article?q={}&Refer=weibo_article',
    ]
    keywords = ["逮虾户", "大庆"]

    def start_requests(self):
        for keyword in self.keywords:
            for url in self.start_urls:
                yield Request(url=url.format(keyword), callback=self.parse)

    def parse(self, response):
        selector = Selector(response)
        page_list = selector.css(".m-page .s-scroll li")
        for page in page_list:
            url = response.request.url + "&" + page.xpath(".//a/@href").extract_first().split("&")[-1]
            if url.split("/")[3] == "weibo":
                yield Request(url=url, callback=self.handle_media_article)
            else:
                yield Request(url=url, callback=self.handle_normal_article)

    def handle_normal_article(self, response):
        selector = Selector(response)
        card_wrap_list = selector.css(".card-wrap")
        for card_wrap in card_wrap_list:
            content = card_wrap.css(".content")
            if not content.extract_first():
                continue
            keyword = get_normal_keyword(response.request.url) + " "
            author = remove_tags(content.xpath(".//div[@class='act']/div[1]/span[1]").extract_first())
            author_url = content.xpath(".//div[@class='act']/div[1]/span[1]/a/@href").extract_first()
            author_url = author_url if author_url else ""
            article_title = remove_tags(card_wrap.xpath(".//div[@class='card-article-a']/h3/a").extract_first(),
                                        keep="em")
            article_detail, article_type = handle_article_detail(content)
            article_url = card_wrap.xpath(".//div[@class='card-article-a']/h3/a/@href").extract_first()
            create_info = content.xpath(".//div[@class='act']")
            create_time = get_time(create_info.xpath(".//div[1]/span[2]/text()").extract_first())
            shares = get_count(create_info.xpath(".//li[1]/a/text()").extract_first())
            stars = get_count(create_info.xpath(".//li[2]/a/span/text()").extract_first())
            affected_count = abs(stars - shares) + max(stars, shares)
            yield WeiboItems(
                keyword=keyword,
                author=author,
                author_url=author_url,
                article_title=article_title,
                article_content="",
                article_detail=article_detail,
                article_url=article_url,
                article_type=article_type,
                article_create_time=create_time,
                affected_count=affected_count,

            )

    def handle_media_article(self, response):
        selector = Selector(response)
        card_wrap_list = selector.css(".card-wrap")
        for card_wrap in card_wrap_list:
            content = card_wrap.css(".content")
            if not card_wrap.xpath("./div[@class='card']/div[@class='card-feed']/div[@class='avator']").extract_first():
                continue
            keyword = get_media_keyword(response.request.url) + " "
            author = content.css(".name::text").extract_first()
            author_url = content.css(".name::attr(href)").extract_first()
            article_title = re.sub(r"\s", "", remove_tags(
                content.css(".txt").extract_first() if content.css(".txt").extract_first() else "", keep="em")).strip()
            article_detail, article_type = handle_article_detail(content)
            create_info = content.xpath("./p[@class='from']")
            create_time = get_time(create_info.xpath("./a[1]/text()").extract_first())
            forwarding = get_count(card_wrap.xpath(".//div[@class='card-act']//li[2]/a/text()").extract_first())
            comments = get_count(card_wrap.xpath(".//div[@class='card-act']//li[3]/a/text()").extract_first())
            stars = get_count(card_wrap.xpath(".//div[@class='card-act']//li[4]/a/em/text()").extract_first())
            # 如何统计受影响人数？简单的将转发、评论、点赞相加吗？我觉得不行，应该将这3者以一定的算法求和，然后相加。
            # 评论的人有极大的可能重复，还有可能对当前微博持反对意见，故取comments * 0.5
            # 点赞和转发的人有3种可能：
            # 1.光点赞不转发
            # 2.光转发不点赞
            # 3.既转发又点赞
            # 故取点赞与转发的最大值+它们的差
            affected_count = comments // 2 + abs(stars - forwarding) + max(stars, forwarding)
            yield WeiboItems(
                keyword=keyword,
                author=author,
                author_url=author_url,
                article_title=article_title,
                article_content="",
                article_detail=article_detail,
                article_url="",
                article_type=article_type,
                article_create_time=create_time
            )