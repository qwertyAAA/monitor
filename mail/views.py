from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from .models import *
import os
from django.db.models import Q
import json
from mail import models
from django.contrib.auth.models import User
from user_management.models import UserInfo
from monitor import settings
from django.core.mail import send_mail
from django.core.files.uploadedfile import TemporaryUploadedFile


# Create your views here.

def pictures(request):
    pictures_list = Pictures.objects.all()

    return render(request, 'mail_pictures/pictures.html', {'pictures_list': pictures_list})


# 邮件图片多选删除
def del_all(request):
    if request.method == 'POST':
        val_obj = request.POST.getlist("check_val")
        url = request.POST.get("url")
        print(val_obj)
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
    return render(request, 'mail_pictures/fhsms.html',
                  {'mail_list': mail_list, 'status_list': status_list})


# 发件箱
def to_mail(request):
    user_id = request.user.id
    user_name_ob = User.objects.filter(pk=user_id).first()
    mail_list = Fhsms.objects.filter(to_user=user_name_ob)
    status_list = StatusMail.objects.filter(nid=0).first()
    return render(request, 'mail_pictures/fhsms.html',
                  {'mail_list': mail_list, 'status_list': status_list})


# 邮件模糊查询
def fuzzy_query(request):
    if request.is_ajax():
        ret = {"status": False, "html": ""}
        search = request.POST.get('search')
        action_time = request.POST.get('action_time')
        end_time = request.POST.get('end_time')
        select_id = request.POST.get('select_id')
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
        print(user_id['id'])
        if from_user:
            Fhsms.objects.create(title=title, content=content, to_user=settings.EMAIL_FROM,
                                 status_id_id=status_id, from_user_id=user_id['id'])
            send_mail(subject=title, message=content, from_email=settings.EMAIL_FROM,
                      recipient_list=from_user)
        return redirect('/fhsms/')
    return render(request, 'mail_pictures/fhsms.html', {'mail_list': mail_list, 'status_list': status_list})

# https://mail.163.com/
def spider_message(request):
    return render(request, 'mail_pictures/Spider_message/spider_message.html')

