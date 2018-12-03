from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from organization import views

urlpatterns = [
    # url(r'^xadmin/', site.urls),
    url(r'^message/', views.message),  # 信息展示
    url(r'^edit_dep/', views.edit),  # 增加
    url(r'^delete_dep/', views.delete),  # 删除
    url(r'^search/', views.search),  # 搜索

]
