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

def classify(request):




    return render(request,'classify.html')