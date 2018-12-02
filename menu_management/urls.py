from django.conf.urls import url
from menu_management import views

urlpatterns=[
    url(r'^check/first/$',views.check_first_menu),
    url(r'^check/second/(\d+)/$',views.check_second_menu),
    url(r'^add/first/$',views.add_first_menu),
    url(r'^add/second/$', views.add_second_menu),
    url(r'^edit/first/(\d+)/$',views.edit_first_menu),
    url(r'^edit/second/(\d+)/$',views.edit_second_menu),
    url(r'^del/first/(\d+)/$',views.del_first_menu),
    url(r'^del/second/(\d+)/$',views.del_second_menu),
]