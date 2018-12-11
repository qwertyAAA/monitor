"""monitor URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.views.static import serve
from django.conf import settings
from mail import views as mali_vi
from xadmin.service.xadmin import x_admin_site as site
from django.conf.urls import url, include
from user_management import urls as user_management_url
from mail import urls as mail_urls
from account.views import *
from account import urls as account_urls
from menu_management import urls as menu_urls
from permission import urls as permission_urls
from organization import urls as organization_urls
from report import urls as report_urls
from SpiderDB import  urls as spider_urls
from fulltext_search import urls as search_urls

urlpatterns = [
    url(r'^xadmin/', site.urls),
    url(r'^menu/', include(menu_urls)),
    url(r'^user_management/', include(user_management_url)),
    url(r'^permission/', include(permission_urls)),
    url(r'^spider/', include(spider_urls)),
    url(r'^account/', include(account_urls)),
    url(r'^organization/', include(organization_urls)),
    url(r'^report/', include(report_urls)),
    url(r'^login/$', login, name="login"),
    url(r'^register/$', register, name="register"),
    url(r'^logout/$', logout, name="logout"),
    url(r'^fhsms/$', mali_vi.fhsms),
    url(r'^fhsms/', include(mail_urls)),
    url(r'^pictures/$', mali_vi.pictures),
    url(r'^pictures/', include(mail_urls)),
    url(r'^fuzzy_query/', mali_vi.fuzzy_query),
    url(r'^fuzzy_query1/', mali_vi.fuzzy_query1),
    url(r'^search/',include(search_urls)),
    url(r'del_all/', mali_vi.del_all),
    # media的相关的路由设置
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    url(r'^upload_img/', mali_vi.upload_img),
    url(r'^$', index),
    url(r'^index/$', index),
    url(r"^get_valid_img.png/", get_valid_img),
]

