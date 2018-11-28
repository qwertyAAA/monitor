from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from organization import views

urlpatterns = [
    # url(r'^xadmin/', site.urls),
    url(r'^message/', views.message),
    url(r'^edit_dep/', views.edit),
    url(r'^delete_dep/', views.delete),
]
