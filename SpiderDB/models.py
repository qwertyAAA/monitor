from django.db import models
from django.contrib.auth.models import User
from user_management.models import UserInfo


# Create your models here.

# 舆情文章表
class Article(models.Model):
    title = models.CharField(max_length=1024)  # 舆情文章标题
    content = models.TextField()  # 舆情文章内容
    detail = models.TextField()  # 文章简介
    url = models.CharField(max_length=1024)  # 文章url
    author = models.ForeignKey(to='Author')  # 文章作者
    create_time = models.DateTimeField()  # 文章的发布时间
    status = models.BooleanField(default=False)  # 状态
    already_read = models.BooleanField(default=False)  # 读取状态
    source = models.ForeignKey(to='Source')  # 文章来源
    affected_count = models.IntegerField(default=0)  # 受影响人数
    keywords = models.CharField(max_length=2048, default="")  # 该文章涉及的关键字
    article_type = models.CharField(max_length=32, default="")  # 该文章的类型，分为纯文本、图文、视频


class Author(models.Model):
    author = models.CharField(max_length=32)
    author_url = models.CharField(max_length=1024)


# 文章的来源    （来源于微博或贴吧等）
class Source(models.Model):
    source = models.CharField(max_length=32)
    source_img = models.FileField(upload_to="avatars/", default="")


# 分类表
class Classify(models.Model):
    title = models.CharField(max_length=32)  # 分类名
    user = models.ManyToManyField(to=User)  # 与用户多对多   页面显示当前用户的所有分类列表


# 方案表
class Rule(models.Model):
    title = models.CharField(max_length=32)  # 方案名
    classify = models.ForeignKey(to=Classify)  # 属于某一个分类
    keyword = models.CharField(max_length=4096)
    exclude_keyword = models.CharField(max_length=1024)
    articles=models.ManyToManyField(to='Article')


# 素材表
class Material(models.Model):
    nid = models.AutoField(primary_key=True)
    user = models.ForeignKey(to=User)
    article = models.ForeignKey(to=Article)


class CollectionArticle(models.Model):
    """
    收藏表
    """
    nid = models.AutoField(primary_key=True)
    user = models.ForeignKey(to=User)
    article = models.ForeignKey(to=Article)
