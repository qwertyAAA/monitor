from django.shortcuts import render
from django.shortcuts import HttpResponse,redirect,render
from menu_management import models
import json
from django.apps import apps
import redis
# Create your views here.


def get_menu():
    # # 得到当前app下面的data类
    # menu_class = apps.get_model('data_manage', 'Data')
    # # 得到data类中的所有字段
    # menu_fields = menu_class._meta.fields
    # menu_list = []
    # for i in menu_fields:
    #     menu_list.append(i.verbose_name)
    menu_list=['test1','test2','test3']
    menu_str=json.dumps(menu_list)
    print(menu_str)