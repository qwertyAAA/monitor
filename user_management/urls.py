from django.conf.urls import url
from . import views

urlpatterns = [
    # 基本操作
    url(r"^main/", views.main),
    url(r"^user_info/", views.user_info),
    url(r"^add_user/", views.aadd_user),
    url(r"^search_user/", views.search_user),
    url(r"^user_search/", views.user_search),
    url(r"^edit_user/(\d+)/$", views.edit_user),
    url(r"^delete_user/(\d+)/$", views.delete_user),
    url(r"^batch_delete/$", views.delete_user),
    # 手机，身份证号，编号 验证
    url(r"^check_usernumber/$", views.check_usernumber),
    url(r"^check_usercard/$", views.check_usercard),
    url(r"^check_userphone/$", views.check_userphone),
    # 邮箱
    url(r"^user_mail/", views.user_mail),
    url(r"^all_email/", views.all_email),
    url(r"^send_message/", views.send_message),
    url(r"^group_sms/", views.group_sms),


    # url(r"^user_mail/$", views.user_mail),
    #  在线
    url(r"^online_users/$", views.online_users),
    url(r'^online_users/search_data/$', views.online_users_search_data),
    url(r'^online_users/(\d+)/delete/$', views.online_users_delete),
    url(r'^online_users/batch_delete/$', views.online_users_batch_delete),
]
