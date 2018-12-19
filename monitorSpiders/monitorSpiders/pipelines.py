# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from .spidersORM import DBSession, Article, Author, Source
import redis


class WeiboPipeline(object):
    def __init__(self):
        self.session = DBSession()
        conn = redis.Redis(host="10.25.116.62", port=6379)
        self.sensitive_words = list(conn.smembers("sensitive_words"))

    def process_item(self, item, spider):
        if spider.name == "weibo":
            author = self.session.query(Author).filter_by(author_url=item["author_url"]).first()
            source = self.session.query(Source).filter_by(source="新浪微博").first()
            if not author:
                author = Author(author=item["author"], author_url=item["author_url"])
                self.add_data(author)
            if not source:
                source = Source(source="新浪微博", source_img="avatars/微博.jpg")
                self.add_data(source)
            article = self.session.query(Article).filter_by(author_id=author.id,
                                                            create_time=item["article_create_time"]).first()
            if not article:
                status = 0
                for obj in self.sensitive_words:
                    if item["article_detail"].find(obj.decode()) != -1:
                        status = 1
                        break
                article = Article(
                    title=item["article_title"],
                    content=item["article_content"],
                    detail=item["article_detail"],
                    url=item["article_url"],
                    author_id=author.id,
                    create_time=item["article_create_time"],
                    already_read=0,
                    # 此处的状态（是否危险）如何判断?
                    status=status,
                    source_id=source.id,
                    affected_count=item["affected_count"],
                    keywords=item["keyword"],
                    article_type=item["article_type"]
                )
                self.add_data(article)
            else:
                keywords = article.keywords
                if keywords.find(item["keyword"]) == -1:
                    keywords += item["keyword"]
                    article.keywords = keywords
                    self.session.commit()

    def close_spider(self, spider):
        self.session.close()

    def add_data(self, data):
        self.session.add(data)
        self.session.commit()


class TiebaPipeline(object):
    def __init__(self):
        conn=redis.Redis(host='10.25.116.62',port=6379)
        print('DB start')
        self.session = DBSession()
        self.sensitive_words=list(conn.smembers('sensitive_words'))

    def process_item(self, item, spider):
        status = 0
        if spider.name=='tieba' or spider.name == 'tieba_all':
            for i in self.sensitive_words:
                if item['article_detail'].find(i.decode()) != -1:
                    status = 1
                    break
            article_url = self.session.query(Article).filter(Article.url == item['article_url']).first()
            # 当文章存在时,判断是否是当前作者写的,如果也是当前作者写的,那么如果关键字不同那么在当前的关键字后面追加新的关键字
            if article_url:
                author_id = article_url.author_id
                author = self.session.query(Author).filter(Author.id == author_id).first()
                author_url = author.author_url
                print(author_url)
                # 判断同一篇文章是否是一个作者写的,如果不是那么插入数据库
                if author_url == item["author_url"]:
                    pass
                    # if article_url.keywords != item['keyword']:
                    #     article_url.keywords = article_url.keywords + ' ' + item['keyword']
                    #     self.session.commit()
                else:
                    article_source = self.session.query(Source).filter(Source.source == item['article_from']).first()
                    if not article_source:
                        article_source = Source(source=item['article_from'],source_img='avtatars/百度.jpg')
                        self.session.add(article_source)
                        self.session.commit()
                    print('DB write')
                    article = Article(
                        title=item["article_title"],
                        content=item["article_content"],
                        detail=item['article_detail'],
                        url=item['article_url'],
                        author_id=author.id,
                        create_time=item["article_create_time"],
                        # 此处的状态（是否危险）如何判断?
                        status=status,
                        source_id=article_source.id,
                        affected_count=item["affected_count"],
                        keywords=item['keyword'],
                        article_type=item['article_type'],

                    )
                    self.session.add(article)
                    self.session.commit()
            else:
                article_source = self.session.query(Source).filter(Source.source == item['article_from']).first()
                if not article_source:
                    article_source = Source(source=item['article_from'])
                    self.session.add(article_source)
                    self.session.commit()
                author = self.session.query(Author).filter(Author.author_url == item['author_url']).first()
                if not author:
                    author = Author(author=item["author"], author_url=item["author_url"])
                    # source = Source(source=item["article_from"])
                    self.session.add(author)
                    self.session.commit()
                print('DB write')
                article = Article(
                    title=item["article_title"],
                    content=item["article_content"],
                    detail=item['article_detail'],
                    url=item['article_url'],
                    author_id=author.id,
                    create_time=item["article_create_time"],
                    # 此处的状态（是否危险）如何判断?
                    status=status,
                    source_id=article_source.id,
                    affected_count=item["affected_count"],
                    keywords=item['keyword'],
                    article_type=item['article_type'],
                )
                self.session.add(article)
                self.session.commit()

    def close_spider(self, spider):
        print('DB close_spider')
        conn=redis.Redis(host='10.25.116.62',port=6379)
        conn.delete('newkeywords')
        self.session.close()
