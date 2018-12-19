from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from report import models
from django.db.models import Q
import time
from datetime import *
from SpiderDB import models as m2
from Myutils.pageutil import Page


# Create your views here.
def index(request):
    obj = models.Report.objects.all()
    page = Page(obj, request, 10, 10)
    sum = page.Sum()
    return render(request, 'report/report_index.html', {
        'obj': sum[0],
        'page_html': sum[1],

    })


def search(request):
    report_name = request.POST.get("report_name", None)
    start_time = request.POST.get("start_time")
    if not start_time:
        start_time = '1972-01-01'
    end_time = request.POST.get("end_time")
    if not end_time:
        end_time = '2050-12-12'
    obj = models.Report.objects.filter(name__contains=report_name, create_time__range=[start_time, end_time])
    return render(request, 'report/report_index.html', {
        'obj': obj
    })


def sucai(request):
    nid = request.user.id
    obj = m2.Material.objects.filter(user_id=nid)
    page = Page(obj, request, 5, 10)
    sum = page.Sum()
    return render(request, 'report/sucai_index.html',
                  {
                      'obj': sum[0],
                      'page_html': sum[1],
                      'len': obj.__len__()
                  })


def mould(request):
    obj = models.Mould.objects.all()
    return render(request, 'report/mould_index.html', {
        'obj': obj,
    })


def cmould(request):
    nid = request.GET.get('nid')
    obj = models.Mould.objects.all()
    for i in obj:
        i.status = 0
        i.save()
    cobj = models.Mould.objects.filter(id=nid).first()
    cobj.status = 1
    cobj.save()
    return redirect('/report/mould/')


def create_report(request):
    uid = request.user.id
    import time
    now_date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    name = '舆情简报' + now_date
    tieba_num = 0
    blog_num = 0
    sensitive = 0
    no_sensitive = 0
    mould_obj = models.Mould.objects.filter(status=1).first()
    if request.is_ajax():
        sucai_list = request.POST.getlist('li')
        for i in sucai_list:
            obj = m2.Article.objects.filter(material__nid=int(i)).first()
            if obj.source.source == '百度贴吧':
                tieba_num += 1
            elif obj.source.source == '新浪微博':
                blog_num += 1

            if obj.status:
                sensitive += 1
            else:
                no_sensitive += 1
        models.Report.objects.create(
            name=name,
            tieba_num=tieba_num,
            blog_num=blog_num,
            sensitive=sensitive,
            no_sensitive=no_sensitive,
            mould=mould_obj
        )
    return JsonResponse({
        'status': 1
    })


def del_rep(request):
    nid = request.GET.get('nid')
    obj = models.Report.objects.filter(id=nid).first()
    obj.delete()
    return JsonResponse({'status': 1})


def rep_detail(request):
    if request.is_ajax():
        nid = request.POST.get('nid')
        obj = models.Report.objects.filter(id=nid).first()
        msg = {
            'id': obj.id,
            'url': obj.mould.url,
            'key': obj.mould.key,
            'create_time': obj.create_time,
            'tieba_num': obj.tieba_num,
            'blog_num': obj.blog_num,
            'sensitive': obj.sensitive,
            'no_sensitive': obj.no_sensitive
        }
        return JsonResponse(msg)


def collection(request):
    uid = request.user.id
    obj = m2.CollectionArticle.objects.filter(user_id=uid)
    page = Page(obj, request, 5, 10)
    sum = page.Sum()
    return render(request, 'report/collection_index.html',
                  {
                      'obj': sum[0],
                      'page_html': sum[1],
                  })


def append(request):
    nid = request.POST.get('nid')
    uid = request.user.id
    msg = {'status': 0}
    obj = m2.Material.objects.filter(user_id=uid, article_id=nid).first()
    if not obj:
        m2.Material.objects.create(
            user_id=uid,
            article_id=nid
        )
        msg['status'] = 1
    return JsonResponse(msg)


def collection_delete(request):
    msg = {'status': 0}
    if request.is_ajax():
        del_list = request.POST.getlist('li')
        for i in del_list:
            obj = m2.CollectionArticle.objects.filter(nid=int(i)).first()
            obj.delete()
    return JsonResponse(msg)


def lot_append(request):
    msg = {'status': 0}
    uid = request.user.id
    if request.is_ajax():
        append_list = request.POST.getlist('li')
        for i in append_list:
            col_obj = m2.CollectionArticle.objects.filter(nid=int(i)).first()
            aid = col_obj.article_id
            obj = m2.Material.objects.filter(user_id=uid, article_id=aid).first()
            if not obj:
                m2.Material.objects.create(
                    user_id=uid,
                    article_id=aid
                )
    return JsonResponse(msg)


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
