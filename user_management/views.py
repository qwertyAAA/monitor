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
        emname = request.POST.get('emname')
        username = request.POST.get('username')
        staff_job = request.POST.get('staff_job')
        staff_job_level = request.POST.get('staff_job_level')

        staff_salary = request.POST.get('staff_salary')
        department_id_list = request.POST.getlist('department_id_list')
        user = models.User.objects.get(username=username)
        print(user)
        UserInfo = models.UserInfo.objects.create(
            staff_name=emname,
            staff_salary=staff_salary,
            staff_job=staff_job,
            staff_job_level=staff_job_level,
            user=user,


        )
        UserInfo.department.set(department_id_list)

        return redirect("/user_management/employee_info/")

    department_list = models.Department.objects.all()
    staff_list = models.UserInfo.objects.all()

    return render(request, "user_management_html/add_user.html", locals())


def main(request):
    return render(request, "base.html")


def user_info(request):
    user_list=models.UserInfo.objects.all()
    page = Page(user_list, request, 10, 10)
    sum = page.Sum()

    return render(request, "user_management_html/user_info.html",{'user_list':sum[0],'page_html':sum[1]})



def edit_user(request, editemp_id):
    edit_staff = models.UserInfo.objects.filter(pk=editemp_id).first()
    if request.method == "POST":
        new_id = request.POST.get('id')
        new_emname = request.POST.get('emname')
        new_username = request.POST.get('username')
        new_staff_job = request.POST.get('staff_job')
        new_staff_job_level = request.POST.get('staff_job_level')

        new_staff_salary = request.POST.get('staff_salary')
        new_department_id_list = request.POST.getlist('department_id_list')

        staffong = models.UserInfo.objects.filter(pk=editemp_id).update(
            # id=new_id,
            staff_name=new_emname,
            staff_salary=new_staff_salary,
            staff_job=new_staff_job,
            staff_job_level=new_staff_job_level,

        )
        staffobj = models.UserInfo.objects.filter(pk=editemp_id).first()
        staffobj.department.set(new_department_id_list)

        return render(request, "user_management/edit_user.html")

    ''' 第一次请求'''

    result = models.Department.objects.all()

    return render(request, "user_management/edit_user.html", locals())


def delete_user(request, num):

    if num:
        '''  对于删除先删除第三张表再删除作者表 id  注意页面的格式问题'''
        del_obj = models.UserInfo.objects.get(id=num)
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
