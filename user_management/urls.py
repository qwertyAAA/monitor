from django.conf.urls import url
from . import views

urlpatterns = [
    url(r"^main/", views.main),
    url(r"^user_info/", views.user_info),
    url(r"^add_user/", views.aadd_user),
    url(r"^online_users/$", views.online_users)
    url(r"^search_user/", views.search_user),
    url(r"^user_search/", views.user_search),
    url(r"^edit_user/(\d+)/$", views.edit_user),
    url(r"^check_usernumber/$", views.check_usernumber),
    url(r"^user_mail/", views.user_mail),
    url(r"^delete_user/(\d+)/$", views.delete_user),
    url(r"^batch_delete/$", views.delete_user),
]
