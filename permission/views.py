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

    # models.Role.objects.filter(Q)

    role_group_id = int(id)                                             #角色组id
    try:
        role_group_obj=models.RoleGroup.objects.get(id=role_group_id)       #该角色组对象,如果id不匹配，异常
    except Exception:
        role_group_obj=models.RoleGroup.objects.all().first()           #接受异常，默认取到数据库内的第一个角色组对象
        role_group_id=role_group_obj.id                                 #获取第一个角色组对象的id
        # return redirect('/permission/role_permission/' + role_group_id + '/')
    role_group_list=models.RoleGroup.objects.all()                      #所有角色组集合
    role_list=models.Role.objects.filter(group_id=role_group_id)        #该角色组下的角色集合
    permission_group_list = models.PermissionGroup.objects.exclude(id=999)  #除了id是999的权限组集合
    crud_permission_list = models.Permission.objects.filter(action='crud')  #增删改查的权限集合
    # print(crud_permission_list)
    role_group_permissions=role_group_obj.permissions.all()             #该角色组的所有权限
    data_permission_list=models.Data_Per.objects.all()
    # print(role_group_permissions)
    # print(permission_group_list)
    return render(request,'role_permission.html',locals())

def role_accredit(request,id):
    role_group_id = request.GET.get('role_group_id')
    role_id=id   #角色id
    role_obj=models.Role.objects.get(id=role_id)
    role_permissions=request.POST.getlist('role_permissions')
    # print(role_permissions)
    for i in role_obj.permissions.all():
        if i.action == 'crud':      #先删除 非菜单权限
            role_obj.permissions.remove(i)
    role_obj.permissions.add(*role_permissions)   #重新添加  增删改查的权限（非菜单权限）
    print(role_obj.permissions.all())
    return redirect('/permission/role_permission/' + role_group_id + '/')

def role_permission_list(request):
    role_id=request.POST.get('role_id')
    print(role_id)
    role_permission_list=models.Role.objects.get(id=role_id).permissions.all().values('id','title')
    print(role_permission_list)
    ret = json.dumps(list(role_permission_list))
    return JsonResponse(ret, safe=False)

def role_del_permission(request,id):
    # return HttpResponse('yes')
    role_group_id = request.GET.get('role_group_id')
    role_id = id  # 角色id
    print('nihao')
    role_obj = models.Role.objects.get(id=role_id)
    role_permissions = request.POST.getlist('role_permissions2')
    print(role_permissions,'********')
    for i in role_permissions:
        role_obj.permissions.remove(i)
    return redirect('/permission/role_permission/' + role_group_id + '/')


def data_permission(request, id):
    role_group_id = request.GET.get('role_group_id')
    role_id = id  # 角色id
    role_obj = models.Role.objects.get(id=role_id)
    data_permission_id=request.POST.get("data_permission")
    role_obj.data_per_id=data_permission_id
    role_obj.save()
    return redirect('/permission/role_permission/' + role_group_id + '/')

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
        # print(permissions)
        for item in permissions:
            for j in permission_list:
                if j == item[0]:
                    permission_list2.append(item[2])
        role_group_obj=models.RoleGroup.objects.get(id=id)
        role_group_obj.permissions.clear()
        role_group_obj.permissions.add(*permission_list2)
        role_list=role_group_obj.role_set.all()
        # print(role_list)

        for role in role_list:
            for i in role.permissions.all():
                if i.action != 'crud':    #如果是菜单权限，就先删除
                    role.permissions.remove(i)
            role.permissions.add(*permission_list2)    #给角色重新添加角色组的菜单权限
            # print(role.permissions.all())
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
    # print(role_id)
    role_obj=models.Role.objects.get(id=role_id)
    # print(role_obj.title)
    role_obj.delete()
    return redirect('/permission/role_permission/' + role_group_id + '/')