from django.conf.urls import url
from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from django.db.models import Q


class ModelXAdmin(object):
    """
        封装给定模型的所有管理选项和功能
    """

    def __init__(self, model, site):
        self.model = model
        self.x_admin_site = site
        self.fields = self.model._meta.fields

    def view(self, request):
        qs = self.model.objects.all()
        data_list = []
        for obj in qs:
            data = []
            for field in self.fields:
                data.append(getattr(obj, field.name))
            data_list.append(data)
        field_names = []
        for field in self.fields:
            field_names.append(field.verbose_name)
        return render(
            request,
            "xadmin/list_view.html",
            {
                "model_name": self.model._meta.model_name,
                "data_list": data_list,
                "field_names": field_names
            }
        )

    def add(self, request):
        pass

    def update(self, request, id):
        pass

    def delete(self, request, id):
        pass

    def search_data(self, request):
        if request.is_ajax():
            keyword = request.POST.get("keyword")
            ret = {"status": False, "html": ""}
            if not len(keyword):
                return JsonResponse(ret)
            ret["status"] = True
            q = Q()
            q.connector = "or"
            for field in self.fields:
                q.children.append((field.verbose_name + "__icontains", keyword))
            qs = self.model.objects.filter(q)
            data_list = []
            for obj in qs:
                data = []
                for field in self.fields:
                    data.append(getattr(obj, field.verbose_name))
                data_list.append(data)
            for data in data_list:
                ret["html"] += """
                    <tr>
                        <td>
                            <input type="checkbox" class="form-group check_item"/>
                        </td>
                """
                for item in data:
                    ret["html"] += """
                        <td>
                            <span>{}</span>
                        </td>
                    """.format(item)
                ret["html"] += """
                <td>
                    <a href="{0}/update" class="btn btn-info">修改</a>
                    <a href="{0}/delete" class="btn btn-danger">删除</a>
                </td>
                </tr>
                """.format(data[0])
            return JsonResponse(ret)

    def get_urls(self):
        temp = []
        temp.append(url(r'^$', self.view))
        temp.append(url(r'add/$', self.add))
        temp.append(url(r'^(\d+)/change/$', self.update))
        temp.append(url(r'^(\d+)/delete/$', self.delete))
        temp.append(url(r'^search_data/', self.search_data))
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

    def __init__(self):
        self._registry = {}  # model_class class -> admin_class instance

    def register(self, model, admin_class=None):
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
            temp.append(url(r'^$', self.index))
            temp.append(url(r'^search_models/', self.search_models))
        return temp

    @property
    def urls(self):
        return self.get_urls(), None, None

    def index(self, request):
        links = []
        for model in self._registry.keys():
            links.append(model._meta.app_label + "/" + model._meta.model_name)
        return render(request, "xadmin/xadmin_index.html", {"links": links})

    def search_models(self, request):
        if request.is_ajax():
            keyword = request.POST.get("keyword")
            ret = {"status": False, "html": ""}
            if not len(keyword):
                return JsonResponse(ret)
            ret["status"] = True
            for model in self._registry.keys():
                model_name = model._meta.model_name
                app_label = model._meta.app_label
                if model_name.find(keyword) != -1:
                    ret["html"] += """
                        <tr>
                            <td>
                                <a href="/xadmin/{0}/{1}">{0}/{1}</a>
                            </td>
                        </tr>
                    """.format(app_label, model_name)
            return JsonResponse(ret)


x_admin_site = XAdminSite()
