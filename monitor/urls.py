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
from xadmin.service.xadmin import x_admin_site as site
from django.conf.urls import url, include
from user_management import urls as user_management_url
from account.views import *
urlpatterns = [
    url(r'^xadmin/', site.urls),
    url(r'^user_management/', include(user_management_url)),
    url(r'^login/$', login, name="login"),
    url(r'^register/$', register, name="register"),
    url(r'^logout/$', logout, name="logout"),
]

