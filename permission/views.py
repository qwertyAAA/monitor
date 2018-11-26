from django.shortcuts import render,redirect,HttpResponse
from user_management.models import UserInfo
from permission import models
from django.contrib.auth.models import User
from django.contrib import auth
from django.http import  JsonResponse
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.db.models import  Q
import json


def user_role(request):
    user_list = User.objects.all()
    role_list=models.Role.objects.all()
    if request.method=='POST':
        user_pk=request.POST.get('user')
        role_list=request.POST.getlist('role')
        user_obj=User.objects.get(pk=user_pk)
        # print(user_obj.role_set.all())
        user_obj.role_set.clear()
        user_obj.role_set.add(*role_list)
        #之后要改为用户管理的系统用户界面
        return redirect('/permission/user_role/')
    return render(request,'user_role.html',locals())


def role_permission(request,id):
    role_group_id = int(id)
    role_group_obj=models.RoleGroup.objects.get(id=role_group_id)
    role_group_list=models.RoleGroup.objects.all()
    role_list=models.Role.objects.filter(group_id=role_group_id)
    permission_group_list = models.PermissionGroup.objects.exclude(id=999)

    role_group_permissions=role_group_obj.permissions.all()
    print(role_group_permissions)
    # print(permission_group_list)
    return render(request,'role_permission.html',locals())


def add_role_group(request):
    if request.method=='POST':
        role_group_title=request.POST.get('role_group_title')
        # print(role_group_title)
        try:
            obj=models.RoleGroup.objects.get(title=role_group_title)
            return HttpResponse('不能添加已有的角色组')
        except Exception:
            models.RoleGroup.objects.create(title=role_group_title)

    return redirect('/permission/role_permission/1/')

def edit_role_group(request,id):
    role_group_id=id
    role_group_title = request.POST.get('role_group_title')
    role_group_obj=models.RoleGroup.objects.get(id=role_group_id)
    role_group_obj.title=role_group_title
    role_group_obj.save()
    return redirect('/permission/role_permission/'+role_group_id+'/')

def delete_role_group(request,id):
    role_group_obj = models.RoleGroup.objects.get(id=id)
    role_group_obj.delete()
    return redirect('/permission/role_permission/1/')

def role_group_permission(request,id):
    if request.method=='POST':
        permission_list=request.POST.getlist('choose')
        permission_list2=[]
        permissions=models.Permission.objects.all().values_list('title','url','id')
        print(permissions)
        for item in permissions:
            for j in permission_list:
                if j == item[0]:
                    permission_list2.append(item[2])
        print(permission_list2)
        role_group_obj=models.RoleGroup.objects.get(id=id)
        role_group_obj.permissions.clear()
        role_group_obj.permissions.add(*permission_list2)

        role_list=role_group_obj.role_set.all()
        print(role_list)
        for role in role_list:
            role.permissions.add(*permission_list2)
    return redirect('/permission/role_permission/'+id+'/')

def edit_role(request,id):
    role_group_id = request.GET.get('role_group_id')
    role_title=request.POST.get('role_title')
    role_id=id
    role_obj=models.Role.objects.get(id=role_id)
    role_obj.title=role_title
    role_obj.save()
    return redirect('/permission/role_permission/' + role_group_id + '/')
def add_role(request):
    role_group_id_old= request.GET.get('role_group_id')
    role_title = request.POST.get('role_title')
    role_group_id = request.POST.get('role_group_id')
    models.Role.objects.create(title=role_title,group_id=role_group_id)
    return redirect('/permission/role_permission/' + role_group_id_old + '/')


def delete_role(request,id):
    role_group_id=request.GET.get('role_group_id')
    role_id=id
    print(role_id)
    role_obj=models.Role.objects.get(id=role_id)
    print(role_obj.title)
    role_obj.delete()
    return redirect('/permission/role_permission/' + role_group_id + '/')