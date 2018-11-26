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
    return render(request, 'second_menu_manage.html', {'menu_list': menu_list})


def add_menu(request):
    menu_title = request.POST.get('menu_name')
    new_menu = models.First_Menu.objects.create(title=menu_title)
    li = '''<tr>
            <td>
                <input type="checkbox">
            </td>
            <td>{0}</td>
            <td><a href="/menu/check/second/{1}/">{2}</a></td>
            <td>
                <a class="btn btn-primary" href="/menu/edit/1/">编辑</a>
                <a class="btn btn-danger" href="/menu/delete/1/">删除</a>
            </td>
        </tr>'''.format(new_menu.nid, new_menu.nid, new_menu.title)
    li2 = '''
        <li>
            <a href="#"><i class="fa fa-sitemap"></i> {{ first.title }}<span class="fa arrow"></span></a>
            <ul class="nav nav-second-level">
                {% for second in first.second_menu_set.all %}
                    <li>
                        <a class="mysecond" href="{{ second.url }}">{{ second.title }}</a>
                    </li>
                {% endfor %}
            </ul>
        </li>
    '''
    rep = {}
    rep['li'] = li
    return JsonResponse(rep)
