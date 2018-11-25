from django.shortcuts import render
from django.shortcuts import HttpResponse,redirect,render
from menu_management import models
import json
from django.apps import apps
import redis
from permission import models as per_models
# Create your views here.


def get_menu(request):
    first_menu=[]
    per_group=per_models.PermissionGroup.objects.all()
    for i in per_group:
        if i.id!=999:
            first_menu.append(i.title)
    print(first_menu)

get_menu()