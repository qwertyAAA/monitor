from django.conf.urls import url
from permission import views as views

urlpatterns = [
    url(r'user_role/$', views.user_role),
    url(r'role_permission/(\d+)/$', views.role_permission),
    url(r'add_role_group/$', views.add_role_group),
    url(r'edit_role_group/(\d+)/$', views.edit_role_group),
    url(r'delete_role_group/(\d+)/$', views.delete_role_group),
    url(r'role_group_permission/(\d+)/$', views.role_group_permission),
    url(r'role_del_permission/(\d+)/$', views.role_del_permission),

    url(r'role_permission_list/$', views.role_permission_list),
    url(r'delete_role/(\d+)/$', views.delete_role),
    url(r'edit_role/(\d+)/$', views.edit_role),
    url(r'role_accredit/(\d+)/$', views.role_accredit),
    url(r'add_role/$', views.add_role),
]
