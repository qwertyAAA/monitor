from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from django.db.models import Q
import time
from datetime import *
from SpiderDB import models as m2


# Create your views here.
def index(request):
    return render(request, 'report/report_index.html')


def search(request):
    report_name = request.POST.get("report_name", None)
    start_time = request.POST.get("start_time")
    end_time = request.POST.get("end_time")
    start_time = datetime.strptime(start_time, "%Y-%m-%d")
    end_time = datetime.strptime(end_time, "%Y-%m-%d")
    print(report_name, start_time, end_time)
    return HttpResponse("查询成功")


def sucai(request):
    nid = request.user.id
    obj = m2.Material.objects.filter(user_id=nid)
    return render(request, 'report/sucai_index.html',
                  {
                      'obj': obj,
                      'len': obj.__len__()
                  })


def mould(request):
    return render(request, 'report/mould_index.html')


def collection(request):
    uid = request.user.id
    obj = m2.ArticleCollection.objects.filter(user_id=uid)
    return render(request, 'report/collection_index.html',
                  {
                      'obj':obj
                  })


def sucai_edit(request):
    nid = request.POST.get('nid')
    obj = m2.Article.objects.filter(id=nid).first()
    if request.is_ajax():
        nid = obj.id
        title = obj.title
        status = obj.status
        ntime = obj.create_time
        source = obj.source.source
        detail = obj.detail
        content = obj.content
        return JsonResponse({
            'nid': nid,
            'title': title,
            'status': status,
            'time': ntime,
            'source': source,
            'detail': detail,
            'content': content
        })
    if request.method == 'POST':
        title = request.POST.get("title")
        kind = request.POST.get("kind")
        source = request.POST.get("source")
        detail = request.POST.get("detail")
        content = request.POST.get("art")
        obj.title = title
        obj.status = 1 if kind == "敏感" else 0
        source_obj = m2.Source.objects.filter(source=source).first()
        obj.source = source_obj
        obj.detail = detail
        obj.content = content
        obj.save()
        return redirect('/report/sucai/')


def delete(request):
    del_id = request.POST.get("del_id")
    obj = m2.Material.objects.filter(nid=del_id).first()
    obj.delete()
    return redirect('/report/sucai/')


def lot_delete(request):
    if request.is_ajax():
        del_list = request.POST.getlist('li')
        for i in del_list:
            obj = m2.Material.objects.filter(nid=int(i)).first()
            obj.delete()
        return redirect('/report/sucai/')


def del_all(request):
    uid = request.user.id
    all_obj = m2.Material.objects.filter(user_id=uid)
    for i in all_obj:
        i.delete()
    return redirect('/report/sucai/')
