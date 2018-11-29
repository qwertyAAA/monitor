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
    return render(request, 'second_menu_manage.html', {'menu_list': menu_list,'id':id})


def add_first_menu(request):
    menu_title = request.POST.get('menu_name')
    new_menu = models.First_Menu.objects.create(title=menu_title)
    return redirect('/menu/check/first/')


def edit_first_menu(request,id):
    menu_id=id
    menu_name = request.POST.get('menu_name')
    print(menu_name, menu_id)
    menu = models.First_Menu.objects.filter(nid=menu_id).first()
    menu.title = menu_name
    menu.save()
    return redirect('/menu/check/first/')


def add_second_menu(request):
    menu_title = request.POST.get('menu_name')
    menu_path=request.POST.get('menu_path')
    menu_id=request.POST.get('menu_id')
    new_menu = models.Second_Menu.objects.create(title=menu_title,url=menu_path,first_menu_id=menu_id)
    return redirect('/menu/check/second/%s/'%new_menu.first_menu_id)


def edit_second_menu(request,id):
    menu_id=id
    menu_name = request.POST.get('menu_name')
    menu_path=request.POST.get('menu_path')
    print(menu_name, menu_id)
    menu = models.Second_Menu.objects.filter(nid=menu_id).first()
    menu.title = menu_name
    menu.url=menu_path
    menu.save()
    return redirect('/menu/check/second/%s/'%menu.first_menu_id)


def del_first_menu(request,id):
    del_id=id
    del_menu=models.First_Menu.objects.get(nid=del_id)
    del_menu.delete()
    return redirect('/menu/check/first/')


def del_second_menu(request,id):
    del_id=id
    print(del_id)
    del_menu=models.Second_Menu.objects.get(nid=del_id)
    first_id=del_menu.first_menu_id
    del_menu.delete()
    return redirect('/menu/check/second/%s/'%first_id)