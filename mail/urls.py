from django.conf.urls import url
from django.contrib import admin
from mail import views as mail_vi

urlpatterns = [
    url(r'chang/id=(\d+)/', mail_vi.chang),
    url(r'del_pictures/id=(\d+)/', mail_vi.del_pictures),
    url(r'del_fhsms/nid=(\d+)/', mail_vi.del_fhsms),
    url(r'to_mail', mail_vi.to_mail),
    url(r'form_mail', mail_vi.form_mail),
]
