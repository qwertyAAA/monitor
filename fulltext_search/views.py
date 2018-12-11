from django.shortcuts import render
from monitorSpiders.monitorSpiders.startTieba import tieba
from SpiderDB import models
import redis
# Create your views here.

key=redis.Redis(host="10.25.116.62",port=6379,max_connections=1000)
def full_search(request):
    if request.method == 'POST':
        keywords=request.POST.get('keywords')
        print(keywords)
        re = key.set('newkeywords1', keywords)
        tieba.start_tieba()
        result=models.Article.objects.filter(keywords=keywords)
        key.delete('newkeywords1')
        return render(request, 'full_search_html.html', {'result': result})
    return render(request,'full_search_html.html')