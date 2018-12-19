from django.conf.urls import url
from . import views

urlpatterns=[
    url(r'^yuqing/$',views.classify),
    url(r'^add_rule/$',views.add_rule),
    url(r'^add_rule2/(\d+)/$',views.add_rule2),
    url(r'^add_classify/$',views.add_classify),
    url(r'^delete_classify/(\d+)/$',views.delete_classify),
    url(r'^delete_rule/(\d+)/$',views.delete_rule),
    url(r'^edit_rule/(\d+)/$',views.edit_rule),
    url(r'^yuqinglist/(\d+)/$',views.yuqinglist),
    url(r'^net_user/$',views.net_user),



]