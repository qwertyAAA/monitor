from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from django.contrib.auth.models import User

from .Myutilss.pageutil import Page

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
def motai(request):
    return render(request,"user_management_html/motai.html")

def add_user(request):
    return render(request,"user_management_html/add_user.html")
def addtest(request):
    return render(request,"user_management_html/edit_user.html")
def aadd_user(request):
    print('czx')
    if request.method == "POST":
        user_id=request.POST.get('user_id')
        user_name = request.POST.get('user_name')
        user_id_card = request.POST.get('user_id_card')
        user_stay_years = request.POST.get('user_stay_years')
        user_gender = request.POST.get('user_gender')
        user_phone=request.POST.get('user_phone')
        user_age = request.POST.get('user_age')
        user_remarks=request.POST.get('user_remarks')
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
    user_list=models.UserInfo.objects.all()
    userlists=models.User.objects.all()
    '''查询所有的用户对应的角色'''
    roles_list=Role.objects.filter(user__userinfo__in=user_list)
    roles_list=Role.objects.all()
    # role
    user_role_dict = {}
    for user in user_list:
        rolelist = Role.objects.filter(user__userinfo=user)
        user_role_dict[user] = rolelist

    page = Page(user_list, request, 10, 10)
    sum = page.Sum()

    return render(request, "user_management_html/user_info.html",{'user_list':sum[0],'page_html':sum[1],"user_role_dict":user_role_dict,'userlists':userlists,'roles_list':roles_list})



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
        new_user_remarks=request.POST.get('user_remarks')
        new_user_address=request.POST.get('user_address')
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
        print(new_roles)
        staffong.first().user.role_set.set(new_roles)
        print(staffong)
        return redirect("/user_management/user_info/")

    ''' 第一次请求'''

    return render(request, "user_management_html/user_info.html", locals())


def delete_user(request, num):

    if num:
        '''  对于删除先删除第三张表再删除作者表 id  注意页面的格式问题'''
        del_obj = models.UserInfo.objects.filter(id=num)

        del_obj.delete()

        return redirect('/user_management/user_info/')
    return redirect('/user_management/user_info/')


def details_user(request, editemp_id):
    edit_staff = models.UserInfo.objects.filter(pk=editemp_id).first()
    result = models.Department.objects.all()
    return render(request, "user_management/details_employee.html", locals())


def search_user(request):
    if request.method == "POST":
        search_key = request.POST.get("search_key")
        print(search_key)
        choice_title = request.POST.get("choice_title")
        if choice_title == "员工编号":
            staff_list = models.UserInfo.objects.filter(id__icontains=search_key)
        elif choice_title == "员工姓名":
            staff_list = models.UserInfo.objects.filter(staff_name__icontains=search_key)
        elif choice_title == "职位名称":
            staff_list = models.UserInfo.objects.filter(staff_job__icontains=search_key)
        elif choice_title == "职务级别":
            staff_list = models.UserInfo.objects.filter(staff_job_level__icontains=search_key)
    return render(request, 'user_management/search_employee.html', locals())


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
