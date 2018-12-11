from django.conf.urls import url
from report import views

urlpatterns = [
    # url(r'^xadmin/', site.urls),
    url(r'^index/', views.index),
    url(r'^search/', views.search),
    url(r'^sucai/', views.sucai),
    url(r'^collection/', views.collection),
    url(r'^mould/', views.mould),
]
