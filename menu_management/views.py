from django.shortcuts import render
from django.shortcuts import HttpResponse, redirect, render
from menu_management import models
from django.http import JsonResponse
import json
from django.apps import apps
import redis
from permission import models as per_models
from Myutils.pageutil import Page

# Create your views here.

def check_first_menu(request):
    menu_list = models.First_Menu.objects.all()
    return render(request, 'first_menu_manage.html', {'menu_list': menu_list})


def check_second_menu(request, id):
    menu_list = models.First_Menu.objects.filter(nid=id)[0].second_menu_set.all()
    return render(request, 'second_menu_manage.html', {'menu_list': menu_list, 'id': id,})


def add_first_menu(request):
    if request.is_ajax():
        menu_title=request.GET.get('menu_name')
        menu = models.First_Menu.objects.filter(title=menu_title).first()
        rep = {}
        rep['span'] = '1'
        if menu:
            return JsonResponse(rep)
        else:
            return JsonResponse({'span':'0'})
    if request.method=='POST':
        menu_title = request.POST.get('menu_name')
        menu_status = request.POST.get('menu_status')
        per_obj=per_models.PermissionGroup.objects.filter(title=menu_title).first()
        if per_obj:
            per_obj.is_del=False
            per_obj.save()
        else:
            per_models.PermissionGroup.objects.create(title=menu_title, action='first')
            per_models.Permission.objects.create(title=menu_title, url=menu_title, action='list',group_id=999)
        if menu_status == '1':
            status = True
        else:
            status = False
        new_menu = models.First_Menu.objects.create(title=menu_title, status=status,action=menu_title)
        return redirect('/menu/check/first/')


def edit_first_menu(request,id):
    if request.is_ajax():
        menu_title=request.GET.get('menu_name')
        menu = models.First_Menu.objects.filter(title=menu_title).first()
        menu_id=request.GET.get('menu_id')
        flag = models.First_Menu.objects.get(nid=menu_id)
        rep = {}
        if menu:
            #排除用户点击输入框却没有进行修改时,也会出现警告的BUG
            if flag.title == menu_title:
                rep['span'] = '0'
                rep['id'] = menu_id
                return JsonResponse(rep)
            rep['span'] = '1'
            rep['id']=menu_id
            return JsonResponse(rep)
        else:
            rep['span'] = '0'
            rep['id'] = menu_id
            return JsonResponse(rep)
    if request.method=='POST':
        menu_id = id
        menu_name = request.POST.get('menu_name')
        menu_status = request.POST.get('menu_status')
        menu = models.First_Menu.objects.filter(nid=menu_id).first()
        permissiongroup = per_models.PermissionGroup.objects.filter(title=menu.title)[0]
        permission = per_models.Permission.objects.filter(title=menu.title)[0]
        menu.title = menu_name
        menu.action = menu_name
        permissiongroup.title = menu_name
        permission.title = menu_name
        permission.url = menu_name
        # permission.group_id=permissiongroup.id
        if menu_status == '1':
            menu.status = True
        else:
            menu.status = False
        menu.save()
        permissiongroup.save()
        permission.save()
        return redirect('/menu/check/first/')


def add_second_menu(request):
    #在用户填写数据时进行校验
    if request.is_ajax():
        menu_title=request.GET.get('menu_name')
        menu_path=request.GET.get('menu_path')
        menu_p=models.Second_Menu.objects.filter(url=menu_path).first()
        menu = models.Second_Menu.objects.filter(title=menu_title).first()
        permission = per_models.Permission.objects.filter(url=menu_path).first()
        rep = {}
        rep['span'] = '1'
        #判断是菜单名和路径是否已经存在
        if menu:
            return JsonResponse(rep)
        elif menu_p:
            return JsonResponse({'span': '2'})
        elif permission:
            return JsonResponse({'span': '2'})
        elif not menu_p:
            return JsonResponse({'span': '3'})
        else:
            return JsonResponse({'span': '0'})
    if request.method=='POST':
        per_title = per_models.PermissionGroup
        menu_title = request.POST.get('menu_name')
        menu_path = request.POST.get('menu_path')
        first_menu_id = request.POST.get('menu_id')
        menu_status = request.POST.get('menu_status')
        per_obj=per_models.Permission.objects.filter(url=menu_path).first()
        if per_obj:
            per_obj.is_del = False
            per_obj.save()
        else:
            first_menu = models.First_Menu.objects.get(nid=first_menu_id)
            per_group = per_models.PermissionGroup.objects.get(title=first_menu.title)
            per_models.PermissionGroup.objects.create(title=menu_title,action='second')
            per_models.Permission.objects.create(title=menu_title,url=menu_path,group_id=per_group.id,action='list_second')
        if menu_status == '1':
            status = True
        elif menu_status == '0':
            status = False
        else:
            status = True
        new_menu = models.Second_Menu.objects.create(title=menu_title, url=menu_path, first_menu_id=first_menu_id, status=status,action=menu_path)
        return redirect('/menu/check/second/%s/' % new_menu.first_menu_id)


def edit_second_menu(request, id):
    if request.is_ajax():
        menu_title=request.GET.get('menu_name')
        menu_id=request.GET.get('menu_id')
        menu_path = request.GET.get('menu_path')
        menu = models.Second_Menu.objects.filter(title=menu_title).first()
        menu_p=models.Second_Menu.objects.filter(url=menu_path).first()
        flag = models.Second_Menu.objects.get(nid=menu_id)
        rep = {}
        if menu:
            #排除用户点击输入框却没有进行修改时,也会出现警告的BUG
            if flag.title == menu_title:
                rep['span'] = '0'
                rep['id'] = menu_id
                return JsonResponse(rep)
            rep['span'] = '1'
            rep['id']=menu_id
            return JsonResponse(rep)
        elif menu_p:
            if flag.url == menu_path:
                rep['span'] = '3'
                rep['id'] = menu_id
                return JsonResponse(rep)
            return JsonResponse({'span': '2','id':menu_id})
        elif not menu_p:
            return JsonResponse({'span': '3','id':menu_id})
        else:
            rep['span'] = '0'
            rep['id'] = menu_id
            return JsonResponse(rep)
    if request.method=='POST':
        menu_id = id
        menu_name = request.POST.get('menu_name')
        menu_path = request.POST.get('menu_path')
        menu_status = request.POST.get('menu_status')
        menu = models.Second_Menu.objects.filter(nid=menu_id).first()
        if menu_status == '1':
            menu.status = True
        else:
            menu.status = False
        #权限表中的url不可以被修改
        permission = per_models.Permission.objects.filter(title=menu.title).first()
        permission.title = menu_name
        menu.title = menu_name
        menu.url = menu_path
        permission.save()
        menu.save()
        return redirect('/menu/check/second/%s/' % menu.first_menu_id)


def del_first_menu(request, id):
    del_id = id
    del_menu = models.First_Menu.objects.get(nid=del_id)
    per_group = per_models.PermissionGroup.objects.filter(title=del_menu.action).first()
    if per_group:
        per_group.is_del = True
        per_group.save()
    del_menu.delete()
    return redirect('/menu/check/first/')


def del_second_menu(request, id):
    del_id = id
    del_menu = models.Second_Menu.objects.get(nid=del_id)
    del_per=per_models.Permission.objects.get(url=del_menu.action)
    del_per.is_del = True
    del_per.save()
    first_id = del_menu.first_menu_id
    del_menu.delete()
    return redirect('/menu/check/second/%s/' % first_id)
