from django.conf.urls import url
from django.views.static import serve
from django.conf import settings

from django.contrib import admin
from mail import views as mail_vi

urlpatterns = [
    url(r'spider_message', mail_vi.spider_message),
    url(r'submit_query', mail_vi.submit_query),
    url(r'add_heart/', mail_vi.add_heart),
    url(r'add_tags/', mail_vi.add_tags),
    url(r'del_one/', mail_vi.del_one),
    url(r'see_eye/', mail_vi.see_eye),
    url(r'spider_del_all/', mail_vi.spider_del_all),
    url(r'spider_add_tags_all/', mail_vi.spider_add_tags_all),
    url(r'spider_change_see/', mail_vi.spider_change_see),
    url(r'spider_add_heart_all/', mail_vi.spider_add_heart_all),
    url(r'(\w+)/article/id=(\d+)/$', mail_vi.article_detail),
]
