from django.conf.urls import url
from django.shortcuts import render, redirect, HttpResponse


class ModelXAdmin(object):
    """
        封装给定模型的所有管理选项和功能
    """

    def __init__(self, model, site):
        self.model = model
        self.x_admin_site = site

    def view(self, request):
        data_list = self.model.objects.all()
        return render(request, "xadmin/list_view.html", {"data_list": data_list})

    def add(self, request):
        return render(request, "xadmin/add_view.html")

    def update(self, request, id):
        return render(request, "xadmin/update_view.html")

    def delete(self, request, id):
        return render(request, "xadmin/delete_view.html")

    def get_urls(self):
        temp = []
        temp.append(url(r'^$', self.view))
        temp.append(url(r'add/$', self.add))
        temp.append(url(r'^(\d+)/change/$', self.update))
        temp.append(url(r'^(\d+)/delete/$', self.delete))
        return temp

    @property
    def urls2(self):
        return self.get_urls(), None, None


class XAdminSite(object):
    """
        自己定义的一个类似于django的
        AdminSet
        用于扩展django的admin模块的功能
    """

    def __init__(self, name='admin'):
        self._registry = {}  # model_class class -> admin_class instance

    def register(self, model, admin_class=None, **options):
        """
            用指定的管理类注册给定的app.models的类
            被注册的应该是一个类，而不是一个对象
            如果没有给出管理类，它将使用默认的ModelXAdmin作为管理类
            被注册的类不应该是一个抽象类
        """
        if not admin_class:
            admin_class = ModelXAdmin
        self._registry[model] = admin_class(model, self)

    def get_urls(self):
        temp = []
        for model, admin_class in self._registry.items():
            app_name = model._meta.app_label
            model_name = model._meta.model_name
            temp.append(url(r'^{0}/{1}/'.format(app_name, model_name), admin_class.urls2))
        return temp

    @property
    def urls(self):
        return self.get_urls(), None, None


x_admin_site = XAdminSite()
