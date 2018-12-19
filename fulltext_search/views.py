from django.shortcuts import render
from monitorSpiders.monitorSpiders.startTieba import tieba
from monitorSpiders.monitorSpiders.startWeibo import starter as weibo
from SpiderDB import models
import redis
import threading
from Myutils.pageutil import Page
from django.http import JsonResponse
import time

# Create your views here.


'''
想法1:通过线程
想法2:通过调用多个爬虫,首先调用爬取页数少的,之后通过前端的定时器或者其他别的方法自动启动另一个爬虫在后台运行
'''
key = redis.Redis(host="10.25.116.62", port=6379, max_connections=1000)


t1 = threading.Thread(target=tieba.start_tieba)
t2 = threading.Thread(target=weibo.start_weibo)

def full_search(request):
    if request.method == 'POST':
        keywords = request.POST.get('keywords')
        re = key.set('newkeywords', keywords)
        # t1.start()
        tieba.start_tieba()
        result = models.Article.objects.filter(keywords=keywords)
        key.delete('newkeywords')
        # page=Page(result,request)
        # sum=page.Sum()
        return render(request, 'full_search_html.html', {'result': result})
    return render(request, 'full_search_html.html')

