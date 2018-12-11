from django.shortcuts import render,redirect,HttpResponse
from user_management.models import UserInfo
from SpiderDB import models
from django.contrib.auth.models import User
from django.contrib import auth
from django.http import  JsonResponse
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.db.models import Q
import json
import redis

def yuqinglist(request,id):
    rule_id = id
    rule_obj = models.Rule.objects.get(id=rule_id)
    if request.method == 'GET':
        key = rule_obj.keyword
        ex_key = rule_obj.exclude_keyword
        # print(key)
        index = key.find('|')
        # print(index)

        key1 = key[:index]  # 或关系
        key2 = key[index + 1:]  # 与关系
        key_huo=''
        key_yu=''
        if 'a-r-e-a-1' in key1:
            ind = key1.find('a-r-e-a-1')
            key11 = key1[ind + 9:]
            ind = key11.find('a-r-e-a-1')
            key12 = key11[:ind]  # 地域字符串
            key_huo+=key12+' '
        if 'p-e-r-s-o-n-1' in key1:
            ind = key1.find('p-e-r-s-o-n-1')
            key21 = key1[ind + 13:]
            ind = key21.find('p-e-r-s-o-n-1')
            key22 = key21[:ind]  # 人物字符串
            key_huo+=key22+' '
        if 'e-v-e-n-t-1' in key1:
            ind = key1.find('e-v-e-n-t-1')
            key31 = key1[ind + 11:]
            ind = key31.find('e-v-e-n-t-1')
            key32 = key31[:ind]  # 人物字符串
            key_huo+=key32+' '
        if 'a-r-e-a-0' in key2:
            ind = key2.find('a-r-e-a-0')
            key11 = key2[ind + 9:]
            ind = key11.find('a-r-e-a-0')
            key12 = key11[:ind]  # 地域字符串
            key_yu+=key12+' '
        if 'p-e-r-s-o-n-0' in key2:
            ind = key2.find('p-e-r-s-o-n-0')
            key21 = key2[ind + 13:]
            ind = key21.find('p-e-r-s-o-n-0')
            key22 = key21[:ind]  # 人物字符串
            key_yu+=key22+' '
        if 'e-v-e-n-t-0' in key2:
            ind = key2.find('e-v-e-n-t-0')
            key31 = key2[ind + 11:]
            ind = key31.find('e-v-e-n-t-0')
            key32 = key31[:ind]  # 人物字符串
            key_yu+=key32+' '

        print(key_huo)
        print(key_yu)
        list_huo=key_huo.split()
        print(list_huo)
        list_yu=key_yu.split()
        print(list_yu)
        list_ex_key=ex_key.split()
        # print(list_ex_key)

        key_words=key_huo+" "+key_yu
        key_lists=list_huo+list_yu
        # print(key_words)
        # print(key_lists)

        list_ke = []
        obj=models.Article.objects.all()

        if len(list_yu)> 0:
            for i in list_yu:
                print(i)
                obj=obj.filter(keywords__contains=i)

            list_ke.append(obj)
            print('************')
            print(list_ke)
            print('************')


        if list_huo.__len__() != 0:
            for i in list_huo:
                ar_list=obj.filter(keywords__contains=i)
                list_ke.append(ar_list)
        print(list_ke)


        # return render(request,'fei/index.html')

        return render(request, 'yuqing.html', locals())






def edit_rule(request,id):
    rule_id = id
    rule_obj = models.Rule.objects.get(id=rule_id)
    if request.method=='GET':
        key=rule_obj.keyword
        ex_key=rule_obj.exclude_keyword
        # print(key)
        index=key.find('|')
        # print(index)

        key1=key[:index]        #或关系
        key2=key[index+1:]      #与关系
        # print(key1)
        # print(key2)
        key_huo = ''
        key_yu = ''
        key12=''
        key22=''
        key32=''
        area_area=1
        person_person=1
        event_event = 1
        if 'a-r-e-a-1' in key1:
            area_area=1
            ind=key1.find('a-r-e-a-1')
            key11=key1[ind+9:]
            ind=key11.find('a-r-e-a-1')
            key12=key11[:ind]   #地域字符串
            print(key12)
            key_huo += key12 + ' '
        if 'p-e-r-s-o-n-1' in key1:
            person_person = 1
            ind=key1.find('p-e-r-s-o-n-1')
            key21=key1[ind+13:]
            ind=key21.find('p-e-r-s-o-n-1')
            key22=key21[:ind]   #人物字符串
            print(key22)
            key_huo += key22 + ' '
        if 'e-v-e-n-t-1' in key1:
            event_event = 1
            ind=key1.find('e-v-e-n-t-1')
            key31=key1[ind+11:]
            ind=key31.find('e-v-e-n-t-1')
            key32=key31[:ind]   #人物字符串
            print(key32)
            key_huo += key32 + ' '
        if 'a-r-e-a-0' in key2:
            area_area = 0
            ind = key2.find('a-r-e-a-0')
            key11 = key2[ind + 9:]
            ind = key11.find('a-r-e-a-0')
            key12 = key11[:ind]  # 地域字符串
            # print(key12)
            key_yu += key12 + ' '
        if 'p-e-r-s-o-n-0' in key2:
            person_person = 0
            ind = key2.find('p-e-r-s-o-n-0')
            key21 = key2[ind + 13:]
            ind = key21.find('p-e-r-s-o-n-0')
            key22 = key21[:ind]  # 人物字符串
            print(key22)
            key_yu += key22 + ' '
        if 'e-v-e-n-t-0' in key2:
            event_event = 0
            ind = key2.find('e-v-e-n-t-0')
            key31 = key2[ind + 11:]
            ind = key31.find('e-v-e-n-t-0')
            key32 = key31[:ind]  # 人物字符串
            # print(key32)
            key_yu += key32 + ' '
        area_key=key12
        person_key=key22
        event_key=key32

        return render(request,'edit_rule.html',locals())

    if request.method=='POST':
        str1=''
        str2=''
        rule_title=request.POST.get('rule_title')
        area_key =request.POST.get('area_key')
        area_radio=request.POST.get('area_radio')
        if area_radio == '1':
            str1+=' a-r-e-a-1 '+area_key+' a-r-e-a-1 '
        else:
            str2 += ' a-r-e-a-0 ' + area_key + ' a-r-e-a-0 '
        person_key=request.POST.get('person_key')
        person_radio=request.POST.get('person_radio')
        if person_radio == '1':
            str1 += ' p-e-r-s-o-n-1 '+person_key+' p-e-r-s-o-n-1 '
        else:
            str2 += ' p-e-r-s-o-n-0 ' + person_key + ' p-e-r-s-o-n-0 '
        event_key=request.POST.get('event_key')
        event_radio=request.POST.get('event_radio')

        if event_radio == '1':
            str1 += ' e-v-e-n-t-1 '+event_key+' e-v-e-n-t-1 '
        else:
            str2 += ' e-v-e-n-t-0 ' + event_key + ' e-v-e-n-t-0 '
        str3=str1+' | '+str2
        key_all=event_key + ' ' + person_key + ' ' + area_key
        conn = redis.Redis(host="10.25.116.62", port=6379)
        conn.rpush("exists_keywords",key_all )
        # print(str3)
        del_key=request.POST.get('del_key')
        rule_obj.title=rule_title
        rule_obj.keyword=str3
        rule_obj.exclude_keyword=del_key
        rule_obj.save()
        return redirect('/spider/yuqing/')




def add_rule2(request,id):
    cla_id=id
    cla_obj = models.Classify.objects.get(id=cla_id)
    if request.method=='POST':
        str1=''
        str2=''
        rule_title=request.POST.get('rule_title')
        area_key =request.POST.get('area_key')
        area_radio=request.POST.get('area_radio')
        key_huo=''
        key_yu=''
        if area_radio == '1':
            str1+=' a-r-e-a-1 '+area_key+' a-r-e-a-1 '
            key_huo+=area_key+' '
        else:
            str2 += ' a-r-e-a-0 ' + area_key + ' a-r-e-a-0 '
            key_yu+=area_key+' '
        person_key=request.POST.get('person_key')
        person_radio=request.POST.get('person_radio')
        if person_radio == '1':
            key_huo+=person_key+' '
            str1 += ' p-e-r-s-o-n-1 '+person_key+' p-e-r-s-o-n-1 '
        else:
            key_yu+=person_key+' '
            str2 += ' p-e-r-s-o-n-0 ' + person_key + ' p-e-r-s-o-n-0 '
        event_key=request.POST.get('event_key')
        event_radio=request.POST.get('event_radio')
        if event_radio == '1':
            key_huo+=event_key+' '
            str1 += ' e-v-e-n-t-1 '+event_key+' e-v-e-n-t-1 '
        else:
            key_yu+=event_key+ ' '
            str2 += ' e-v-e-n-t-0 ' + event_key + ' e-v-e-n-t-0 '
        str3=str1+' | '+str2
        # print(str3)
        del_key=request.POST.get('del_key')
        key_all=event_key+' '+person_key+' '+area_key
        conn = redis.Redis(host="10.25.116.62", port=6379)
        conn.rpush("exists_keywords",key_all )
        # conn.rpush("exists_keywords", person_key)
        # conn.rpush("exists_keywords", area_key)
        models.Rule.objects.create(title=rule_title,keyword=str3,exclude_keyword=del_key,classify=cla_obj)

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

def delete_rule(request,id):
    rule_obj=models.Rule.objects.get(id=id)
    rule_obj.delete()
    return redirect('/spider/yuqing/')


def add_classify(request):
    if request.method == 'POST':
        new_classify=request.POST.get('new_classify')
        obj=models.Classify.objects.create(title=new_classify)
        user=request.user
        user.classify_set.add(obj)
    return redirect('/spider/yuqing/')



def classify(request):
    # classify_list=models.Classify.objects.all()
    return render(request,'classify.html',locals())