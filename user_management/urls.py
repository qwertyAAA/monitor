from django.conf.urls import url
from . import views


urlpatterns = [
     url(r"^main/", views.main),
     url(r"^motai/", views.motai),
     url(r"^user_info/", views.user_info),
     url(r"^add_user/", views.add_user),
     url(r"^addtest/", views.addtest),
     url(r"^edit_user/(\d+)/$", views.edit_user),
     url(r"^delete_user/(\d+)/$", views.delete_user),
]