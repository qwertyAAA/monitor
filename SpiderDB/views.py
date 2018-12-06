from django.shortcuts import render,redirect,HttpResponse
from user_management.models import UserInfo
from SpiderDB import models
from django.contrib.auth.models import User
from django.contrib import auth
from django.http import  JsonResponse
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.db.models import  Q
import json
def add_rule2(request,id):
    cla_id=id
    cla_obj = models.Classify.objects.get(id=cla_id)
    if request.method=='POST':
        str1=''
        str2=''
        rule_title=request.POST.get('rule_title')
        area_radio=request.POST.get('area_radio')
        if area_radio == '1':
            str1+=rule_title
            str1+=' '
        else:
            str2 += rule_title
            str2 += ' '
        person_key=request.POST.get('person_key')
        person_radio=request.POST.get('person_radio')
        if person_radio == '1':
            str1 += person_key
            str1 += ' '
        else:
            str2 += person_key
            str2 += ' '
        event_key=request.POST.get('event_key')
        event_radio=request.POST.get('event_radio')
        if event_radio == '1':
            str1 += event_key
            str1 += ' '
        else:
            str2 += event_key
            str2 += ' '
        str3=str1+'|'+str2
        del_key=request.POST.get('del_key')

        return redirect('/spider/yuqing/')


def add_rule(request):
    if request.method == 'POST':
        classify_id=request.POST.get('choose_cla')
        cla_obj=models.Classify.objects.get(id=classify_id)
        classify_list = models.Classify.objects.all()
    return render(request,'add_rule.html',locals())


def delete_classify(request,id):
    cla_obj=models.Classify.objects.get(id=id)
    cla_obj.delete()
    return redirect('/spider/yuqing/')


def add_classify(request):
    if request.method == 'POST':
        new_classify=request.POST.get('new_classify')
        models.Classify.objects.create(title=new_classify)
    return redirect('/spider/yuqing/')



def classify(request):
    classify_list=models.Classify.objects.all()
    return render(request,'classify.html',locals())