from django.conf.urls import url
from . import views

urlpatterns = [
    url(r"^main/", views.main),
    url(r"^motai/", views.motai),
    url(r"^user_info/", views.user_info),
    url(r"^add_user/", views.aadd_user),
    url(r"^online_user/", views.online_user),
    url(r"^search_user/", views.search_user),
    url(r"^user_search/", views.user_search),
    url(r"^edit_user/(\d+)/$", views.edit_user),
    url(r"^delete_user/(\d+)/$", views.delete_user),
]
