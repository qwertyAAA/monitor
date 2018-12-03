# Create your views here.
from django.shortcuts import render, redirect, HttpResponse
''' 发送站内信需要导入的包'''
from mail.models import Fhsms, StatusMail
from django.contrib.auth.models import User
from django.conf import settings
from django.core.mail import send_mail

'''当导入这个方法的时候：用的时候必须是  models.表明'''

from . import models
def user_mail(touser,title,content,from_user,status_id):
    status_list = StatusMail.objects.all()
    touser = touser
    print(touser)
    title = title
    content = content
    from_user = from_user
    status_id = status_id  # 默认未读
    user_id = User.objects.filter(email=from_user[0]).values("id").first()
    if user_id:
        Fhsms.objects.create(title=title, content=content, to_user=touser,
                             status_id_id=status_id, from_user_id=user_id["id"])
        send_mail(subject=title, message=content, from_email=settings.EMAIL_FROM,
                  recipient_list=from_user)
