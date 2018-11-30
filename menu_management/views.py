from django.shortcuts import render
from django.shortcuts import HttpResponse, redirect, render
from menu_management import models
from django.http import JsonResponse
import json
from django.apps import apps
import redis
from permission import models as per_models


# Create your views here.

def check_first_menu(request):
    menu_list = models.First_Menu.objects.all()
    return render(request, 'first_menu_manage.html', {'menu_list': menu_list})


def check_second_menu(request, id):
    menu_list = models.First_Menu.objects.filter(nid=id)[0].second_menu_set.all()
    return render(request, 'second_menu_manage.html', {'menu_list': menu_list, 'id': id})


def add_first_menu(request):
    if request.method=='GET':
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
        if menu_status == '1':
            status = True
        else:
            status = False
        new_menu = models.First_Menu.objects.create(title=menu_title, status=status)
        return redirect('/menu/check/first/')


def edit_first_menu(request, id):
    menu_id = id
    menu_name = request.POST.get('menu_name')
    menu_status = request.POST.get('menu_status')
    print(menu_status)
    menu = models.First_Menu.objects.filter(nid=menu_id).first()
    menu.title = menu_name
    if menu_status == '1':
        menu.status = True
    else:
        menu.status = False
    menu.save()
    return redirect('/menu/check/first/')


def add_second_menu(request):
    per_title = per_models.PermissionGroup
    menu_title = request.POST.get('menu_name')
    menu_path = request.POST.get('menu_path')
    menu_id = request.POST.get('menu_id')
    menu_status = request.POST.get('menu_status')
    per_obj=per_models.Permission.objects.filter(url=menu_path).first()
    if per_obj:
        per_obj.is_del=False
    if menu_status == '1':
        status = True
    else:
        status = False
    print(status)
    new_menu = models.Second_Menu.objects.create(title=menu_title, url=menu_path, first_menu_id=menu_id, status=status,action=menu_path)
    return redirect('/menu/check/second/%s/' % new_menu.first_menu_id)


def edit_second_menu(request, id):
    menu_id = id
    menu_name = request.POST.get('menu_name')
    menu_path = request.POST.get('menu_path')
    menu_status = request.POST.get('menu_status')
    print(menu_name, menu_id)
    menu = models.Second_Menu.objects.filter(nid=menu_id).first()
    if menu_status == '1':
        menu.status = True
    else:
        menu.status = False
    menu.title = menu_name
    menu.url = menu_path
    menu.save()
    return redirect('/menu/check/second/%s/' % menu.first_menu_id)


def del_first_menu(request, id):
    del_id = id
    del_menu = models.First_Menu.objects.get(nid=del_id)
    per_group = per_models.PermissionGroup.objects.filter(title=del_menu.action).first()
    if per_group:
        per_group.is_del=True
        per_group.save()
    del_menu.delete()
    return redirect('/menu/check/first/')


def del_second_menu(request, id):
    del_id = id
    print(del_id)
    del_menu = models.Second_Menu.objects.get(nid=del_id)
    del_per=per_models.Permission.objects.get(url=del_menu.url)
    del_per.is_del = True
    del_per.save()
    first_id = del_menu.first_menu_id
    del_menu.delete()
    return redirect('/menu/check/second/%s/' % first_id)
