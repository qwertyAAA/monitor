from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from .models import *
from SpiderDB.models import *
import time
import os
from django.db.models import Q
from django.core import serializers
import json
from mail import models
from django.contrib.auth.models import User
from user_management.models import UserInfo
from monitor import settings
from django.core.mail import send_mail
from Myutils.pageutil import Page
from django.core.files.uploadedfile import TemporaryUploadedFile


# Create your views here.

def pictures(request):
    pictures_list = Pictures.objects.all()
    page = Page(pictures_list, request, 10, 10)
    sum = page.Sum()
    return render(request, 'mail_pictures/pictures.html', {'pictures_list': sum[0], 'page_html': sum[1]})


# def base(request):
#     user_id = request.user.id
#     fhsms_list = Fhsms.objects.all()
#     sum_email = 0
#     print(user_id)
#     for i in range(len(fhsms_list)):
#         sum_email += 1
#     print(sum_email)
#     return render(request, 'base.html',
#                   {'fhsms_list': fhsms_list, 'sum_email': sum_email})


# 邮件图片多选删除
def del_all(request):
    if request.method == 'POST':
        val_obj = request.POST.getlist("check_val")
        url = request.POST.get("url")
        if url == '/fhsms/':
            for i in val_obj:
                del_obj = models.Fhsms.objects.filter(id=i)
                del_obj.delete()
        if url == '/pictures/':
            for i in val_obj:
                del_obj = models.Pictures.objects.filter(id=i)
                del_obj.delete()
    return render(request, 'mail_pictures/fhsms.html')


def send_all(request):
    # 获取登录用户的cookie信息
    # 获取到登录用户的邮箱
    pass


# 图片

def upload_img(request):
    if request.method == 'POST':
        master_id = request.user.id
        print(master_id)
        obj = request.FILES.get('files')
        print(obj)
        form1 = request.FILES.get('form')
        print(form1)
        obj_name = request.POST.get('files_name')
        # media路径下的图片 回传到富文本 json数据格式   服务器上图片的路径  img的方式回传到
        # 构建服务器的图片的路径
        models.Pictures.objects.create(master_id_id=master_id, title=obj_name, name=obj_name, path=obj)
        # *************************************************************
        # for i in range(len(obj)):
        # request.FILES.get(obj[i])
        # models.Pictures.objects.create(master_id_id=session_id, name=nameArr[i], path=obj[i])
        # *************************************************************
        # path = os.path.join(settings.MEDIA_ROOT, obj.name)
        # with open(path, 'wb') as f:
        #     for line in obj:
        #         f.write(line)
        # result = {
        #     "error": 0,
        #     "url": '/media/' + obj.name
        # }
        # Pictures.objects.create(master_id_id=master_id, name=obj.name)
    return HttpResponse("ok")


def chang(request, num):
    print(1)
    Fhsms.objects.filter(id=num).update(status_id_id='1')
    return redirect('/fhsms/')


def del_pictures(request, num):
    if num:
        del_obj = models.Pictures.objects.filter(id=num)
        del_obj.delete()
        return redirect('/pictures/')
    return HttpResponse('ok')


def del_fhsms(request, num):
    print(num)
    if num:
        del_obj = models.Fhsms.objects.filter(id=num)
        del_obj.delete()
        return redirect('/fhsms/')
    return HttpResponse('ok')


# 收件箱
def form_mail(request):
    user_id = request.user.id
    mail_list = Fhsms.objects.filter(from_user_id=user_id)
    status_list = StatusMail.objects.filter(nid=0).first()
    page = Page(mail_list, request, 10, 10)
    sum = page.Sum()
    return render(request, 'mail_pictures/fhsms.html',
                  {'mail_list': sum[0], 'status_list': status_list, 'page_html': sum[1]})


# 发件箱
def to_mail(request):
    user_id = request.user.id
    user_name_ob = User.objects.filter(pk=user_id).first()
    mail_list = Fhsms.objects.filter(to_user=user_name_ob)
    status_list = StatusMail.objects.filter(nid=0).first()
    page = Page(mail_list, request, 10, 10)
    sum = page.Sum()
    return render(request, 'mail_pictures/fhsms.html',
                  {'mail_list': sum[0], 'status_list': status_list, 'page_html': sum[1]})


# 邮件模糊查询
def fuzzy_query(request):
    if request.is_ajax():
        ret = {"status": False, "html": ""}
        search = request.POST.get('search')
        action_time = request.POST.get('action_time')
        end_time = request.POST.get('end_time')
        select_id = request.POST.get('select_id')
        print(search)
        print(select_id)
        count = 0
        q = Q()
        q.connector = "or"
        if not search and not action_time and not end_time and select_id == 0:
            q.children.append(('status_id__icontains', select_id))
            return JsonResponse(ret)
        elif not search and not action_time and not end_time and select_id == 1:
            q.children.append(('status_id__icontains', '未读'))
            return JsonResponse(ret)
        elif not search and not action_time and not end_time and select_id == 2:
            q.children.append(('status_id__icontains', '已读'))
            return JsonResponse(ret)
        elif search:
            q.children.append(('title__icontains', search))
            q.children.append(('to_user__icontains', search))
        fhsms = Fhsms.objects.filter(q)
        ret["status"] = True
        for obj in fhsms:
            count += 1
            check_box = """
                    <input type="checkbox" value="{}" id="onclick_checkbox" name="onclick_checkbox">
                """.format(obj.id)
            button = """
                    <button type="button" class="btn btn-info" data-toggle="modal"
                                data-target="#search-one{count}" id="one_search"
                                value="">查询
                    </button>
                    <a href="https://mail.163.com/">
                        <button type="button" class="btn btn-warning">回复</button>
                    </a>
                """.format(count=count)
            ret["html"] += """
                    <tr>
                        <td>{check_box}</td>
                        <td>{counter}</td>
                        <td>{title}</td>
                        <td>{to_user}</td>
                        <td>{from_user}</td>
                        <td>{create_time}</td>
                        <td>{status}</td>
                        <td>{button}</td>
                    </tr>
                """.format(
                check_box=check_box,
                counter=count,
                title=obj.title,
                to_user=obj.to_user,
                from_user=obj.from_user,
                create_time=obj.create_time,
                status=obj.status_id.status,
                button=button,
            )
        return JsonResponse(ret)


# 图片模糊查询
def fuzzy_query1(request):
    if request.is_ajax():
        ret = {"status": False, "html": ""}
        search = request.POST.get('search')
        action_time = request.POST.get('action_time')
        end_time = request.POST.get('end_time')
        count = 0
        q = Q()
        q.connector = "or"
        if search:
            q.children.append(('title__icontains', search))
            q.children.append(('name__icontains', search))
            q.children.append(('BZ__icontains', search))
        pi = Pictures.objects.filter(q)
        ret["status"] = True
        for obj in pi:
            count += 1
            check_box = """
                    <input type="checkbox" value="{}" id="onclick_checkbox" name="onclick_checkbox">                
            """.format(obj.id)
            button = """
                    <button type="button" class="btn btn-info" data-toggle="modal"
                                    data-target="#search-pictures{count}" id="pictures_search"
                                    value="">查询
                            </button>
                    <a href="pictures/del_pictures/id={pi_id}/">
                        <button type="button" class="btn btn-danger">删除</button>
                    </a>
                """.format(count=count, pi_id=obj.id)
            img = """
                    <img class="media-object" src="/media/{path}" alt="..."
                                 style="width: 52px;height: 52px;">
            """.format(path=obj.path)
            ret["html"] += """
                    <tr>
                        <td>{check_box}</td>
                        <td>{counter}</td>
                        <td>{img}</td>
                        <td>{title}</td>
                        <td>{name}</td>
                        <td>{create_time}</td>
                        <td>{username}</td>
                        <td>{BZ}</td>
                        <td>{button}</td>
                    </tr>
                """.format(
                check_box=check_box,
                counter=count,
                img=img,
                title=obj.title,
                name=obj.name,
                create_time=obj.create_time,
                username=obj.master_id.username,
                BZ=obj.BZ,
                button=button,
            )
        return JsonResponse(ret)


# 邮件的发送
def fhsms(request):
    mail_list = Fhsms.objects.all()
    status_list = StatusMail.objects.filter(nid=0).first()
    page = Page(mail_list, request, 10, 10)
    sum = page.Sum()
    # response = redirect('/fhsms/')
    # 设置cookie，关闭游览器自动失效
    # response.set_cookie('key', 'value')
    # print(response)
    if request.method == 'POST':
        title = request.POST.get("title")
        content = request.POST.get("content")
        from_user = request.POST.getlist("from_user")
        status_id = request.POST.get("status_id")  # 默认未读
        user_id = User.objects.filter(email=from_user[0]).values('id').first()
        print(status_id)
        if from_user:
            Fhsms.objects.create(title=title, content=content, to_user=settings.EMAIL_FROM,
                                 status_id_id=status_id, from_user_id=user_id['id'])
            send_mail(subject=title, message=content, from_email=settings.EMAIL_FROM,
                      recipient_list=from_user)
        return redirect('/fhsms/')
    return render(request, 'mail_pictures/fhsms.html',
                  {'mail_list': sum[0], 'page_html': sum[1], 'status_list': status_list})


# ************************************************************8
# 舆情信息展示


# https://mail.163.com/
def spider_message(request):
    message_list = Article.objects.all()
    material = Material.objects.all()
    page = Page(message_list, request, 10, 10)
    sum = page.Sum()
    # keywords = Material.objects.filter(id=material[0].id).values('keywords')
    return render(request, 'mail_pictures/Spider_message/spider_message.html',
                  {'message_list': sum[0], 'page_html': sum[1], 'material': material})


# 舆情条件查询
def submit_query(request):
    # 获取当前时间戳
    new_time = int(time.time())
    message_list = []
    if request.is_ajax():
        arr_click = request.POST.getlist("arr_click")
        time_size = arr_click[0]            # 时间范围
        article_ranking = arr_click[1]      # 文章排序
        attribute_right = arr_click[2]      # 敏感信息
        results_show = arr_click[3]         # 结果呈现
        merge_right = arr_click[4]          # 相似文章
        micro_blog = arr_click[5]           # 转发微博
        involve_right = arr_click[6]        # 涉及方式
        region = arr_click[7]               # 信源区域
        matching_right = arr_click[8]       # 匹配方式
        blog_content = arr_click[9]         # 微博内容
        source_website = arr_click[10]      # 来源网站
        # source_message = arr_click[11]    # 来源信息
        # fields = []
        # for field in Article._meta.fields:
        #     fields.append(field.name)
        if time_size == "今日" and article_ranking == "智能排序" and micro_blog == "显示" and source_website == "全部":
            message_list = serializers.serialize("json", Article.objects.order_by("title"))

            # message = {}
            # for item in Article.objects.order_by("title"):
            #     for field in fields:
            #         message[field] = getattr(item, field)
            #     print(message)
            #     message_list.append(message)
        # elif time_size == "今日" and article_ranking == "时间降序" and micro_blog == "显示" and source_website == "全部":
        #     message_list["message"] = Article.objects.order_by("-create_time")
        # elif time_size == "今日" and article_ranking == "时间升序" and micro_blog == "显示" and source_website == "全部":
        #     message_list["message"] = Article.objects.order_by("create_time")
        # elif time_size == "今日" and article_ranking == "采集顺序" and micro_blog == "显示" and source_website == "全部":
        #     message_list["message"] = Article.objects.order_by("id")
        # elif time_size == "今日" and article_ranking == "智能排序" and micro_blog == "显示" and source_website == "贴吧":
        #     message_list["message"] = Article.objects.filter(socure_id='2').order_by("title")
        # elif time_size == "今日" and article_ranking == "时间降序" and micro_blog == "显示" and source_website == "贴吧":
        #     message_list["message"] = Article.objects.filter(socure_id='2').order_by("-create_time")
        # elif time_size == "今日" and article_ranking == "时间升序" and micro_blog == "显示" and source_website == "贴吧":
        #     message_list["message"] = Article.objects.filter(socure_id='2').order_by("create_time")
        # elif time_size == "今日" and article_ranking == "采集顺序" and micro_blog == "显示" and source_website == "贴吧":
        #     message_list["message"] = Article.objects.filter(socure_id='2').order_by("id")
        # elif time_size == "今日" and article_ranking == "智能排序" and micro_blog == "显示" and source_website == "微博":
        #     message_list["message"] = Article.objects.filter(socure_id='1').order_by("title")
        # elif time_size == "今日" and article_ranking == "时间降序" and micro_blog == "显示" and source_website == "微博":
        #     message_list["message"] = Article.objects.filter(socure_id='1').order_by("-create_time")
        # elif time_size == "今日" and article_ranking == "时间升序" and micro_blog == "显示" and source_website == "微博":
        #     message_list["message"] = Article.objects.filter(socure_id='1').order_by("create_time")
        # elif time_size == "今日" and article_ranking == "采集顺序" and micro_blog == "显示" and source_website == "微博":
        #     message_list["message"] = Article.objects.filter(socure_id='1').order_by("id")
    return JsonResponse(message_list, safe=False)


# 加入收藏
def add_heart(request):
    user_id = request.user.id
    if request.is_ajax():
        message_id = request.POST.get("message_id")
        CollectionArticle.objects.create(article_id=message_id, user_id=user_id)
    return HttpResponse("OK")


# 加入简报
def add_tags(request):
    user_id = request.user.id
    if request.is_ajax():
        message_id = request.POST.get("message_id")
        Material.objects.create(article_id=message_id, user_id=user_id)
    return HttpResponse("ok")


# 标为已读
def see_eye(request):
    if request.is_ajax():
        message_id = request.POST.get('message_id')
        Article.objects.filter(id=message_id).update(already_read=True)
    return HttpResponse("OK")


# 单个删除舆情信息
def del_one(request):
    if request.is_ajax():
        message_id = request.POST.get('message_id')
        del_obj = Article.objects.filter(id=message_id).first()
        del_obj.delete()
    return HttpResponse("OK")


# 批量删除
def spider_del_all(request):
    if request.method == 'POST':
        val_obj = request.POST.getlist("check_val")
        print(type(val_obj))
        for i in val_obj:
            print(1)
            del_obj = Article.objects.filter(id=i).first()
            print(del_obj)
            del_obj.delete()
    return render(request, 'mail_pictures/Spider_message/spider_message.html')


# 批量加入收藏
def spider_add_heart_all(request):
    if request.is_ajax():
        user_id = request.user.id
        val_obj = request.POST.getlist("check_val")
        for i in val_obj:
            CollectionArticle.objects.create(article_id=i, user_id=user_id)
    return HttpResponse("ok")


# Article详情页
def article_detail(request, title, num):
    print(title)
    print(num)
    return HttpResponse('ok')


# 批量标为已读
def spider_change_see(request):
    if request.is_ajax():
        val_obj = request.POST.getlist("check_val")
        for i in val_obj:
            Article.objects.filter(id=i).update(already_read=True)
    return HttpResponse("ok")


# 批量加入简报素材
def spider_add_tags_all(request):
    if request.is_ajax():
        user_id = request.user.id
        val_obj = request.POST.getlist("check_val")
        for i in val_obj:
            Material.objects.create(article_id=i, user_id=user_id)
    return HttpResponse("ok")
