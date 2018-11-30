from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

from .Myutilss.pageutil import Page
from online_management.online_users import online_user_management
'''当导入这个方法的时候：用的时候必须是  models.表明'''
# from user_management import models
from . import models
from django.apps import apps

''' 当导入这个时候跟上面的区别是直接用不用加.'''
# from .models import *
from django import forms
from django.forms import widgets
from permission.models import Role
from django.forms import ModelForm
from middlewares.online_users_management import online_users_management


def user_mail(request):
    return render(request, "user_management_html/user_mail.html")


def online_user(request):
    online_users = online_user_management.users
    return render(request, "user_management_html/online_user.html", locals())


def search_user(request):
    return render(request, "user_management_html/search_user.html")


def aadd_user(request):
    print('czx')

    if request.method == "POST":
        user_id = request.POST.get('user_id')
        user_name = request.POST.get('user_name')
        user_number = request.POST.get('adduser_number')
        user_id_card = request.POST.get('user_id_card')
        user_stay_years = request.POST.get('user_stay_years')
        user_gender = request.POST.get('user_gender')
        user_phone = request.POST.get('user_phone')
        user_age = request.POST.get('user_age')
        user_remarks = request.POST.get('user_remarks')
        titlelist = request.POST.getlist('titlelist')
        user = models.User.objects.get(id=user_id)


        UserInfo = models.UserInfo.objects.create(
            user_name=user_name,
            user_id_card=user_id_card,
            user_stay_years=user_stay_years,
            user_gender=user_gender,
            user_phone=user_phone,
            user_age=user_age,
            user_remarks=user_remarks,
            user_number=user_number,
            user=user,
        )
        ''' 怎么向Role表里面添加信息'''
        # UserInfo.user.role_set(titlelist)
        UserInfo.user.role_set.add(*titlelist)
        print("正确")
        return redirect("/user_management/user_info/")

    print('cuiwu ')
    return render(request, "user_management_html/user_info.html", locals())


def main(request):
    return render(request, "base.html")


def user_info(request):
    user_list = models.UserInfo.objects.all()
    userlists = models.User.objects.all()
    '''查询所有的用户对应的角色'''
    roles_list = Role.objects.filter(user__userinfo__in=user_list)
    roles_list = Role.objects.all()
    user_role_dict = {}
    for user in user_list:
        rolelist = Role.objects.filter(user__userinfo=user)
        user_role_dict[user] = rolelist

    page = Page(user_list, request, 10, 10)
    sum = page.Sum()

    return render(request, "user_management_html/user_info.html",
                  {'user_list': sum[0], 'page_html': sum[1], "user_role_dict": user_role_dict, 'userlists': userlists,
                   'roles_list': roles_list})


def edit_user(request, user_id):
    print('编辑页面')
    edit_user = models.UserInfo.objects.filter(pk=user_id).first()
    if request.method == "POST":
        new_id = request.POST.get('id')
        new_user_name = request.POST.get('user_name')
        new_username = request.POST.get('username')
        new_user_phone = request.POST.get('user_phone')
        new_user_age = request.POST.get('user_age')
        new_user_id_card = request.POST.get('user_id_card')
        new_user_remarks = request.POST.get('user_remarks')
        new_user_address = request.POST.get('user_address')
        new_roles = request.POST.getlist('roles')

        staffong = models.UserInfo.objects.filter(pk=user_id)
        staffong.update(
            # id=new_id,
            user_name=new_user_name,
            user_phone=new_user_phone,
            user_age=new_user_age,
            user_id_card=new_user_id_card,
            user_remarks=new_user_remarks,
            user_address=new_user_address,

        )
        # userobj = models.UserInfo.objects.filter(pk=user_id).first()
        # staffong.user.role_set.add(*new_roles)
        # print(new_roles)
        staffong.first().user.role_set.set(new_roles)
        # print(staffong)
        return redirect("/user_management/user_info/")

    ''' 第一次请求'''

    return render(request, "user_management_html/user_info.html", locals())


def delete_user(request, num=None):
    if num:
        '''  对于删除先删除第三张表再删除作者表 id  注意页面的格式问题'''
        del_obj = models.UserInfo.objects.filter(id=num)

        del_obj.delete()

        return redirect('/user_management/user_info/')
    if request.is_ajax():
        delete_id_list = request.POST.getlist("delete_id_list")
        for delete_id in delete_id_list:
            models.UserInfo.objects.filter(id=delete_id).delete()
        return JsonResponse({"status": True})
    return JsonResponse({"status": False})


def details_user(request, editemp_id):
    edit_staff = models.UserInfo.objects.filter(pk=editemp_id).first()
    result = models.Department.objects.all()
    return render(request, "user_management/details_employee.html", locals())


def user_search(request):
    if request.method == "POST":
        search_key = request.POST.get("search_key")
        if search_key:
            choice_title = request.POST.get("choice_title")
            print(choice_title, "************")
            if choice_title == "用户编号":
                userlists = models.UserInfo.objects.filter(user_number__icontains=search_key)
            elif choice_title == "用户姓名":
                userlists = models.UserInfo.objects.filter(user_name__icontains=search_key)
            elif choice_title == "用户住址":
                userlists = models.UserInfo.objects.filter(user_address__icontains=search_key)
            elif choice_title == "用户年龄":
                userlists = models.UserInfo.objects.filter(user_age__icontains=search_key)
                roles_lists = Role.objects.all()

        return render(request, 'user_management_html/search_user.html', locals())


def batch(request):
    if request.method == "POST":
        action = request.POST.get("action")
        print(action)
        selected_pk = request.POST.getlist("select_pk")
        print(selected_pk)
        if action == "批量删除":
            print('czx')
            # for i in selected_pk:
            result = models.UserInfo.objects.filter(pk__in=selected_pk).delete()
            print(result)

        return redirect('/user_management/employee_info/')  # 所有的对象

    return render(request, "user_management/user_info.html")


def online_users(request):
    online_users = online_users_management.users
    return render(request, "user_management_html/online_users.html", locals())

  
@csrf_exempt
def check_usernumber(request):
    data = {}
    print(request.is_ajax())
    if request.is_ajax():
        if request.method == "POST":
            adduser_number = request.POST.get("adduser_number", None)
            user = models.UserInfo.objects.filter(user_number=adduser_number)
            if user:
                data["message"] = 1
            else:
                data["message"] = 0
    print(data)
    return JsonResponse(data)
