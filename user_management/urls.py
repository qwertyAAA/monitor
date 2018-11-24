from django.conf.urls import url
from user_management import views

urlpatterns = [
     url(r"^main/", views.main),
     url(r"^user_info/", views.user_info),
     url(r"^add_user/", views.add_user),
     url(r"^edit_user/(\d+)/$", views.edit_user),
     url(r"^delete_user/(\d+)/$", views.delete_user),
]