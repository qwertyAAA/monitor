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
    return render(request, 'mail_pictures/pictures.html')


# 图片
def upload(request):
    obj = request.FILES.get('upload_img')
    # media路径下的图片 回传到富文本 json数据格式   服务器上图片的路径  img的方式回传到
    # 构建服务器的图片的路径
    path = os.path.join(settings.MEDIA_ROOT, obj.name)
    with open(path, 'wb') as f:
        for line in obj:
            f.write(line)
    result = {
        "error": 0,
        "url": '/media/' + obj.name
    }
    return JsonResponse(result)


# 邮件的发送
def fhsms(request):
    mail_list = Fhsms.objects.all()
    status_list = StatusMail.objects.filter(nid=0).first()
    print(status_list)
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
