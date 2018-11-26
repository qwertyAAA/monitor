from django.conf.urls import url
from menu_management import views

urlpatterns=[
    url(r'^check/first/',views.check_first_menu),
    url(r'^check/second/(\d+)/',views.check_second_menu),
    url(r'^add/first/',views.add_menu)
]