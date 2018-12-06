from django.db import models
from django.contrib.auth.models import User
from user_management.models import UserInfo


# Create your models here.

# 舆情文章表
class Article(models.Model):
    title = models.CharField(max_length=128)  # 舆情文章标题
    content = models.TextField()  # 舆情文章内容
    url = models.CharField(max_length=1024)  # 文章url
    author = models.ForeignKey(to='Author')  # 文章作者
    create_time = models.DateTimeField()  # 文章的发布时间
    status = models.BooleanField(default=False)  # 状态
    source = models.ForeignKey(to='Source')  # 文章来源
    affected_count = models.IntegerField(default=0)  # 受影响人数


class Author(models.Model):
    author = models.CharField(max_length=32)
    author_url = models.CharField(max_length=1024)


# 文章的来源    （来源于微博或贴吧等）
class Source(models.Model):
    source = models.CharField(max_length=32)


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
