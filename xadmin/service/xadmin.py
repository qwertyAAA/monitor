from django.conf.urls import url
from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from django.db.models import Q
from django import forms
from django.db.models import OneToOneField, ForeignKey, ManyToManyField
import datetime
from django.contrib.auth.hashers import make_password


class ModelXAdmin(object):
    """
        封装给定模型的所有管理选项和功能
    """
    field_names = []

    def __init__(self, model, site):
        self.model = model
        self.x_admin_site = site
        if self.field_names:
            self.fields = []
            # 借助python的特性实现的查找功能，时间复杂度为O(n)
            for field in self.model._meta.fields:
                if field.name == self.field_names[0]:
                    self.fields.append(field)
                    self.field_names.pop()
        else:
            self.fields = [field for field in self.model._meta.fields]
        self.cross_table_fields = []
        for field in self.fields:
            if isinstance(field, ManyToManyField) or isinstance(field, OneToOneField) or isinstance(field, ForeignKey):
                self.cross_table_fields.append(field)

    def list_view(self, request):
        current_app_label = self.model._meta.app_label
        current_model_name = self.model._meta.model_name
        qs = self.model.objects.all()
        data_list = []
        for obj in qs:
            data = []
            for field in self.fields:
                if field.name.find("password") != -1:
                    continue
                data.append(getattr(obj, field.name))
            data_list.append(data)
        field_names = []
        for field in self.fields:
            if field.name.find("password") != -1:
                continue
            field_names.append(field.verbose_name)
        return render(
            request,
            "xadmin/list_view.html",
            {
                "current_url": current_app_label + "/" + current_model_name + "/",
                "model_name": self.model._meta.model_name,
                "data_list": data_list,
                "field_names": field_names
            }
        )

    def get_form(self, request=None, instance=None):
        """
        用于获取一个XAdminFrom对象



        :param request: 当前请求
        :param instance: 一个QuerySet实例
        :return: 一个XAdminFrom对象
        """

        class XAdminFrom(forms.ModelForm):
            class Meta:
                model = self.model
                fields = [field.name for field in self.fields]

        if request and instance:
            form = XAdminFrom(data=request.POST, instance=instance)
        elif request:
            form = XAdminFrom(data=request.POST)
        elif instance:
            form = XAdminFrom(instance=instance)
        else:
            form = XAdminFrom()
        return form

    def add(self, request):
        cross_tables_info = []
        for field in self.cross_table_fields:
            cross_tables_info.append({
                "app_label": getattr(self.model, field.name).field.remote_field.model._meta.app_label,
                "model_name": getattr(self.model, field.name).field.remote_field.model._meta.model_name,
                "verbose_name": field.verbose_name
            })
        current_app_label = self.model._meta.app_label
        current_model_name = self.model._meta.model_name
        form = self.get_form()
        if request.method == "POST":
            form = self.get_form(request)
            if form.is_valid():
                password = form.cleaned_data.get("password")
                form.save(commit=False)
                for field in self.fields:
                    if "password" in field.name:
                        setattr(form.instance, field.name, make_password(password))
                form.instance.save()
                form.save_m2m()
            return redirect("/xadmin/" + current_app_label + "/" + current_model_name + "/")
        return render(request, "xadmin/update_view.html", locals())

    def update(self, request, pk):
        cross_tables_info = []
        for field in self.cross_table_fields:
            cross_tables_info.append({
                "app_label": getattr(self.model, field.name).field.remote_field.model._meta.app_label,
                "model_name": getattr(self.model, field.name).field.remote_field.model._meta.model_name,
                "verbose_name": field.verbose_name
            })
        current_app_label = self.model._meta.app_label
        current_model_name = self.model._meta.model_name
        qs = self.model.objects.filter(pk=pk).first()
        form = self.get_form(instance=qs)
        if request.method == "POST":
            form = self.get_form(request=request, instance=qs)
            if form.is_valid():
                password = form.cleaned_data.get("password")
                form.save(commit=False)
                for field in self.fields:
                    if "password" in field.name:
                        setattr(form.instance, field.name, make_password(password))
                form.instance.save()
                form.save_m2m()
            return redirect("/xadmin/" + current_app_label + "/" + current_model_name + "/")
        return render(request, "xadmin/update_view.html", locals())

    def delete(self, request, pk=None):
        if request.is_ajax():
            delete_id_list = request.POST.getlist("delete_id_list")
            if delete_id_list:
                for delete_id in delete_id_list:
                    self.model.objects.filter(pk=delete_id).delete()
                return JsonResponse({"status": True})
            self.model.objects.filter(pk=pk).delete()
            return JsonResponse({"status": True})

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
                # 思路2存在的问题的解决方法：
                if field in self.cross_table_fields:
                    print(field)
                    continue
                else:
                    q.children.append((field.name + "__icontains", keyword))
            # 此处代码应该可以优化。
            # 问题：如何查询跨表字段中是否包含keyword
            # 思路1：在每个model中将__str__中返回的字段作为一个类属性，然后在此处处理时就会很轻松
            # 思路2（解决方法）：先从表中查询所有的数据，然后对跨表的数据进行判断，返回判断为True的model对象
            # 思路2存在的问题：需要查询一遍整个表，虽然QuerySet的惰性机制和缓存机制已经减少了很多冗余的操作
            qs = []
            for obj in self.model.objects.filter(q):
                qs.append(obj)
            for obj in self.model.objects.all():
                for field in self.cross_table_fields:
                    if getattr(obj, field.name).__str__().find(keyword) != -1 and obj not in qs:
                        qs.append(obj)
            print(self.cross_table_fields)
            data_list = []
            for obj in qs:
                data = []
                for field in self.fields:
                    data.append(getattr(obj, field.name))
                data_list.append(data)
            for data in data_list:
                ret["html"] += """
                    <tr>
                        <td>
                            <input type="checkbox" class="check_item"/>
                        </td>
                """
                for item in data:
                    # 此处为返回前端的数据进行过滤
                    item = item[:40:] if isinstance(item, str) else item
                    item = item.strftime("%Y-%m-%d %H:%M") if isinstance(item, datetime.datetime) else item
                    # try:
                    #     item = item.strftime("%Y{0}%m{1}%d{2} %H:%M".format("年", "月", "日"))
                    # except Exception as e:
                    #     item = item
                    #     print(e)
                    ret["html"] += """
                        <td>
                            <span >{}</span>
                        </td>
                    """.format(item)
                ret["html"] += """
                <td>
                    <a href="{0}/update" class="btn btn-info">修改</a>
                    <button class="btn btn-danger for_delete" delete_id="{0}">删除</button>
                </td>
                </tr>
                """.format(data[0])
            return JsonResponse(ret)

    def get_urls(self):
        temp = []
        temp.append(url(r'^$', self.list_view))
        temp.append(url(r'add/$', self.add))
        temp.append(url(r'^(\d+)/update/$', self.update))
        temp.append(url(r'^(\d+)/delete/$', self.delete))
        temp.append(url(r'^batch_delete/$', self.delete))
        temp.append(url(r'^search_data/$', self.search_data))
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
        return render(request, "xadmin/xadmin_index.html", locals())

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
                if model_name.find(keyword) != -1 or app_label.find(keyword) != -1:
                    ret["html"] += """
                        <tr>
                            <td>
                                <a href="/xadmin/{0}/{1}">{0}/{1}</a>
                            </td>
                        </tr>
                    """.format(app_label, model_name)
            return JsonResponse(ret)


x_admin_site = XAdminSite()
