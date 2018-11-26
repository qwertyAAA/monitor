from django.conf.urls import url
from permission import views as views

urlpatterns = [
    url(r'user_role/$', views.user_role),
    url(r'role_permission/(\d+)/$', views.role_permission),
    url(r'add_role_group/$', views.add_role_group),
    url(r'edit_role_group/(\d+)/$', views.edit_role_group),
    url(r'delete_role_group/(\d+)/$', views.delete_role_group),
    url(r'role_group_permission/(\d+)/$', views.role_group_permission),
    url(r'delete_role/(\d+)/$', views.delete_role),
    url(r'edit_role/(\d+)/$', views.edit_role),
    url(r'add_role/$', views.add_role),
]
