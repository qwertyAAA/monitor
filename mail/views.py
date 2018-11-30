from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from .models import *
import os
import json
from mail import models
from django.contrib.auth.models import User
from user_management.models import UserInfo
from django.conf import settings
from django.core.mail import send_mail


# Create your views here.

def pictures(request):
    pictures_list = Pictures.objects.all()

    return render(request, 'mail_pictures/pictures.html', {'pictures_list': pictures_list})


# 邮件多选删除
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
                del_obj = models.Fhsms.objects.filter(id=i)
                del_obj.delete()
    return render(request, 'mail_pictures/fhsms.html')


def send_all(request):
    # 获取登录用户的cookie信息
    # 获取到登录用户的邮箱
    pass


# 图片

def upload_img(request):
    if request.method == 'POST':
        session_id = request.user.userinfo.id
        nameArr = request.POST.getlist('nameArr')
        obj = request.FILES.getlist('imgArr')
        # media路径下的图片 回传到富文本 json数据格式   服务器上图片的路径  img的方式回传到
        # 构建服务器的图片的路径
        # *************************************************************

        # for i in range(len(obj)):
        # request.FILES.get(obj[i])
        # models.Pictures.objects.create(master_id_id=session_id, name=nameArr[i], path=obj[i])
        print(obj)
        # *************************************************************
        # path = os.path.join(settings.MEDIA_ROOT, obj.name)
        #         # with open(path, 'wb') as f:
        #         #     for line in obj:
        #         #         f.write(line)
        #         # result = {
        #         #     "error": 0,
        #         #     "url": '/media/' + obj.name
        #         # }
        #         # Pictures.objects.create(master_id_id=session_id)
    return render(request, 'mail_pictures/pictures.html')


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
        status_id = request.POST.get("status_id")
        user_id = User.objects.filter(email=from_user[0])
        userinfo_id = UserInfo.objects.filter(user=user_id).first()
        if userinfo_id:
            Fhsms.objects.create(title=title, content=content, to_user=settings.EMAIL_FROM,
                                 status_id_id=status_id, from_user=userinfo_id)
            send_mail(subject=title, message=content, from_email=settings.EMAIL_FROM,
                      recipient_list=from_user)
            return redirect('/fhsms/')
    return render(request, 'mail_pictures/fhsms.html', {'mail_list': mail_list, 'status_list': status_list})

# https://mail.163.com/

