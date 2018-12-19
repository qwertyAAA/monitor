''' 数据分析库'''
''' 在matplotlib的图中设置中文标签 start'''
from matplotlib.font_manager import FontProperties

font = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=15)
'''在matplotlib的图中设置中文标签 end '''
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
from pandas import Series, DataFrame
import pandas as pd
# Create your views here.
from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_exempt
from middlewares.all_requests import all_requests
from .Myutilss.pageutil import Page
from permission.models import Role
from mail.models import Fhsms
from SpiderDB.models import Article

''' 发送站内信需要导入的包'''
from mail.models import Fhsms, StatusMail
from django.contrib.auth.models import User
from django.conf import settings
from django.core.mail import send_mail
from Myutils.pageutil import Page

'''当导入这个方法的时候：用的时候必须是  models.表明'''
from . import models

''' 当导入这个时候跟上面的区别是直接用不用加.'''


#
# def user_mail(request):
#     return render(request, "user_management_html/user_mail.html")
def search_user(request):
    return render(request, "user_management_html/search_user.html")


''' 添加用户'''


def aadd_user(request):
    if request.method == "POST":
        user_id = request.POST.get('user_id')
        user_name = request.POST.get('user_name')
        user_number = request.POST.get('adduser_number')
        user_id_card = request.POST.get('ckuser_id_card')
        user_stay_years = request.POST.get('user_stay_years')
        user_gender = request.POST.get('user_gender')
        user_phone = request.POST.get('ckuser_phone')
        user_age = request.POST.get('user_age')
        user_remarks = request.POST.get('user_remarks')
        titlelist = request.POST.getlist('titlelist')
        user = models.User.objects.get(id=user_id)

        UserInfo = models.UserInfo.objects.create(
            user_name=user_name,
            user_id_card=user_id_card,
            user_stay_years=user_stay_years,
            user_gender=user_gender,
            user_phone=user_phone,
            user_age=user_age,
            user_remarks=user_remarks,
            user_number=user_number,
            user=user,
        )
        ''' 怎么向Role表里面添加信息'''
        # UserInfo.user.role_set(titlelist)
        UserInfo.user.role_set.add(*titlelist)
        print("正确")
        return redirect("/user_management/user_info/")

    print('cuiwu ')
    return render(request, "user_management_html/user_info.html", locals())


def main(request):
    return render(request, "base.html")


''' 用户角色'''


def user_info(request):
    # user_list = models.UserInfo.objects.all()
    from permission.service.DataPermission import has_data
    ret = has_data(request)
    user_list = ret['user_list']
    userlists = models.User.objects.all()
    '''查询所有的用户对应的角色'''
    roles_list = Role.objects.filter(user__userinfo__in=user_list)
    roles_list = Role.objects.all()
    user_role_dict = {}
    for user in user_list:
        rolelist = Role.objects.filter(user__userinfo=user)
        user_role_dict[user] = rolelist

    page = Page(user_list, request, 10, 10)
    sum = page.Sum()

    return render(request, "user_management_html/user_info.html",
                  {'user_list': sum[0], 'page_html': sum[1], "user_role_dict": user_role_dict, 'userlists': userlists,
                   'roles_list': roles_list})


''' 编辑页面'''


def edit_user(request, user_id):
    print('编辑页面')
    edit_user = models.UserInfo.objects.filter(pk=user_id).first()
    if request.method == "POST":
        new_id = request.POST.get('id')
        new_user_name = request.POST.get('user_name')
        new_username = request.POST.get('username')
        new_user_phone = request.POST.get('user_phone')
        new_user_age = request.POST.get('user_age')
        new_user_id_card = request.POST.get('user_id_card')
        new_user_remarks = request.POST.get('user_remarks')
        new_user_address = request.POST.get('user_address')
        new_roles = request.POST.getlist('roles')

        staffong = models.UserInfo.objects.filter(pk=user_id)
        staffong.update(
            # id=new_id,
            user_name=new_user_name,
            user_phone=new_user_phone,
            user_age=new_user_age,
            user_id_card=new_user_id_card,
            user_remarks=new_user_remarks,
            user_address=new_user_address,

        )
        # userobj = models.UserInfo.objects.filter(pk=user_id).first()
        # staffong.user.role_set.add(*new_roles)
        # print(new_roles)
        staffong.first().user.role_set.set(new_roles)
        # print(staffong)
        return redirect("/user_management/user_info/")

    ''' 第一次请求'''

    return render(request, "user_management_html/user_info.html", locals())


''' 删除页面'''


def delete_user(request, num=None):
    if num:
        '''  对于删除先删除第三张表再删除作者表 id  注意页面的格式问题'''
        del_obj = models.UserInfo.objects.filter(id=num)

        del_obj.delete()

        return redirect('/user_management/user_info/')
    if request.is_ajax():
        delete_id_list = request.POST.getlist("delete_id_list")
        for delete_id in delete_id_list:
            models.UserInfo.objects.filter(id=delete_id).delete()
        return JsonResponse({"status": True})
    return JsonResponse({"status": False})


''' 用户详情'''


def details_user(request, editemp_id):
    edit_staff = models.UserInfo.objects.filter(pk=editemp_id).first()
    result = models.Department.objects.all()
    return render(request, "user_management/details_employee.html", locals())


''' 模糊查询'''


def user_search(request):
    if request.method == "POST":
        search_key = request.POST.get("search_key")
        if search_key:
            choice_title = request.POST.get("choice_title")
            print(choice_title, "************")
            if choice_title == "用户编号":
                userlists = models.UserInfo.objects.filter(user_number__icontains=search_key)
            elif choice_title == "用户姓名":
                userlists = models.UserInfo.objects.filter(user_name__icontains=search_key)
            elif choice_title == "用户住址":
                userlists = models.UserInfo.objects.filter(user_address__icontains=search_key)
            elif choice_title == "用户年龄":
                userlists = models.UserInfo.objects.filter(user_age__icontains=search_key)
                roles_lists = Role.objects.all()

        return render(request, 'user_management_html/search_user.html', locals())


def batch(request):
    if request.method == "POST":
        action = request.POST.get("action")

        selected_pk = request.POST.getlist("select_pk")

        if action == "批量删除":
            print('czx')
            # for i in selected_pk:
            result = models.UserInfo.objects.filter(pk__in=selected_pk).delete()
            print(result)

        return redirect('/user_management/employee_info/')  # 所有的对象

    return render(request, "user_management/user_info.html")


''' 统计在线人数返回页面'''


def online_users(request):
    online_users = []
    for other_request in all_requests.requests_list:
        if other_request.user not in online_users:
            online_users.append(other_request.user)
    return render(request, "user_management_html/online_users.html", locals())


@csrf_exempt
def check_usernumber(request):
    data = {}
    if request.is_ajax():
        adduser_number = request.POST.get("adduser_number", None)
        user = models.UserInfo.objects.filter(user_number=adduser_number).first()
        if user:
            data["message"] = 1
        else:
            data["message"] = 0
        print(data["message"])
        return JsonResponse(data)


''' 0'''


@csrf_exempt
def check_userphone(request):
    print('czxcczxczxczxcz')
    data = {}
    print(request.is_ajax())

    if request.is_ajax():
        user_phone = request.POST.get("ckuser_phone", None)
        print(type(user_phone))
        if len(user_phone) == 11:
            user = models.UserInfo.objects.filter(user_phone=user_phone).first()
            if user:
                data["message"] = 1
            else:
                data["message"] = 0
            print(data["message"])
            return JsonResponse(data)
        else:
            data["message"] = 1

        return JsonResponse(data)


@csrf_exempt
def check_usercard(request):
    data = {}
    if request.is_ajax():
        user_id_card = request.POST.get("user_id_card", None)
        user = models.UserInfo.objects.filter(user_id_card=user_id_card).first()
        if user:
            data["message"] = 1
        else:
            data["message"] = 0
        print(data["message"])
        return JsonResponse(data)


''' 0'''

# def online_users_search_data(request):
#     if request.is_ajax():
#         print('czx')
#         keyword = request.POST.get("keyword")
#         ret = {"status": False, 'html': ""}
#         if not keyword:
#             return JsonResponse(ret)
#         ret['status'] = True
#         users = online_users_management.users
#         for obj in users:
#             print(obj,'xxxxxxxx')
#             print(type(obj))
#             check_box = """
#             <td>
#                 <input type="checkbox" class="check_item" delete_id="{}"/>
#             </td>""".format(obj.pk)
#             operation = """
#                 <a href="{0}/delete/" class="btn btn-danger for_delete" delete_id="{0}">下线</a>
#             """.format(obj.pk)
#             ret["html"] += """
#             <tr>
#             {check_box}
#             <td>
#             {username}
#             </td>
#             <td>
#             {email}
#             </td>
#             <td>
#             {phone}
#             </td>
#             <td>
#             {operation}
#             </td>
#         </tr>
#         """.format(
#                 check_box=check_box if obj != request.user else "<td></td>",
#                 username=obj.username,
#                 email=obj.email,
#                 phone=obj.userinfo.user_phone,
#                 operation=operation if obj != request.user else "<td></td>"
#             )
#             print('xxxxxxxxxccccccccccccccccccccccccccccccc')
#         return JsonResponse(ret)
''' 在线查询'''


def online_users_search_data(request):
    if request.is_ajax():
        keyword = request.POST.get("keyword")
        ret = {"status": False, 'html': ""}
        if not keyword:
            return JsonResponse(ret)
        ret['status'] = True
        users = []
        for other_request in all_requests.requests_list:
            if other_request.user.pk in all_requests.requests_user_pk:
                if other_request.user.username.find(keyword) != -1:
                    users.append(other_request.user)
                elif other_request.user.email.find(keyword) != -1:
                    users.append(other_request.user)
                elif hasattr(other_request.user, "userinfo"):
                    if other_request.user.userinfo.user_phone != -1:
                        users.append(other_request.user)
        for obj in users:
            check_box = """
            <td>
                <input type="checkbox" class="check_item" delete_id="{}"/>
            </td>""".format(obj.pk)
            operation = """
                <a href="{0}/delete/" class="btn btn-danger for_delete" delete_id="{0}">下线</a>
            """.format(obj.pk)
            ret["html"] += """
            <tr>
            {check_box}
            <td>
            {username}
            </td>
            <td>
            {email}
            </td>
            <td>
            {phone}
            </td>
            <td>
            {operation}
            </td>
        </tr>
        """.format(
                check_box=check_box if obj != request.user else "<td></td>",
                username=obj.username,
                email=obj.email,
                phone=obj.userinfo.user_phone if hasattr(obj, "userinfo") else "",
                operation=operation if obj != request.user else "<td></td>"
            )
        return JsonResponse(ret)


''' 批量下线'''


def online_users_batch_delete(request):
    if request.is_ajax():
        delete_id_list = request.POST.getlist("delete_id_list")
        for delete_id in delete_id_list:
            for other_request in all_requests.requests_list:
                if other_request.user.pk == int(delete_id):
                    all_requests.requests_list.remove(other_request)
                    all_requests.requests_user_pk.remove(other_request.user.pk)
                    logout(other_request)
    return JsonResponse({"status": True})


'''  单个下线'''


def online_users_delete(request, delete_id):
    for item in all_requests.requests_list:
        if item.user.pk == int(delete_id):
            all_requests.requests_list.remove(item)
            all_requests.requests_user_pk.remove(item.user.pk)
            logout(item)
    return redirect("/user_management/online_users/")


# def mail(request):
#     print('zzzzzzzzzzzzzzzzzzzzzzzzzzz')
#     data={}
#     mail_list = Fhsms.objects.all()
#     status_list = StatusMail.objects.filter(nid=0).first()
#     # if request.is_ajax():
#     # return JsonResponse(data)
#
#         # response = redirect('/fhsms/')
#         # 设置cookie，关闭游览器自动失效
#         # response.set_cookie('key', 'value')
#         # print(response)
#      if request.method == 'POST':
#             touser=request.user
#             title = request.POST.get("title")
#             username = request.POST.get('username')
#             content = request.POST.get("content")
#
#             from_user = request.POST.getlist("from_user")
#             status_id = request.POST.get("status_id")    # 默认未读
#             user_id = User.objects.filter(email=from_user[0]).first()
#             if user_id:
#                 Fhsms.objects.create(title=title, content=content, to_user=touser,
#                                      status_id_id=status_id, from_user=user_id)
#                 send_mail(subject=title, message=content, from_email=settings.EMAIL_FROM,
#                           recipient_list=from_user)
#                 data['message']=1
#                 return redirect('/fhsms/')
#             else:
#                 data['message']=0
#
#      return render(request, 'mail_pictures/fhsms.html', {'mail_list': mail_list, 'status_list': status_list})
#

''' 单一发送站内信'''


def user_mail(request):
    status_list = StatusMail.objects.all()
    if request.method == 'POST':
        touser = request.user
        print(touser)
        title = request.POST.get("title")
        content = request.POST.get("content")
        from_user = request.POST.getlist("from_user")
        status_id = request.POST.get("status_id")  # 默认未读
        user_id = User.objects.filter(email=from_user[0]).values("id").first()
        if user_id:
            Fhsms.objects.create(title=title, content=content, to_user=touser,
                                 status_id_id=status_id, from_user_id=user_id["id"])
            send_mail(subject=title, message=content, from_email=settings.EMAIL_FROM,
                      recipient_list=from_user)

            return redirect('/user_management/user_info/')
    return render(request, 'user_management_html/user_info.html', {"status_list": status_list})


def allemail(request):
    print('开始群发站内信')
    status_list = StatusMail.objects.all()
    ''' 这样的值难道不被选中吗'''

    if request.method == 'POST':
        userlist_pk = request.POST.getlist('select_pk')
        print('选中的值呢')
        print(userlist_pk)

        for user_pk in userlist_pk:
            userobj = models.UserInfo.objects.filter(id=user_pk)
            print(userobj)

            touser = request.user
            print(touser)
            title = request.POST.get("title")
            content = request.POST.get("content")
            ''' 邮箱不能再前端动态的获取因为是群发必须在循环里面取到'''
            # from_user = request.POST.getlist("from_user") #邮箱
            from_user = userobj.user.email
            print(from_user, '邮箱邮箱邮箱有用喜爱那个')
            status_id = request.POST.get("status_id")  # 默认未读
            user_id = User.objects.filter(email=from_user[0]).values("id").first()
            print(user_id["id"])
            if user_id:
                Fhsms.objects.create(title=title, content=content, to_user=touser,
                                     status_id_id=status_id, from_user_id=user_id["id"])
                send_mail(subject=title, message=content, from_email=settings.EMAIL_FROM,
                          recipient_list=from_user)

                return redirect('/user_management/user_info/')
        print('end0')
    print('end1')

    return render(request, 'user_management_html/user_info.html', {"status_list": status_list})


'''群发站内信 '''


def all_email(request):
    print('开始群发站内信')
    from user_management import allEmail
    if request.is_ajax():
        userinfo_list = request.POST.getlist("delete_id_list")
        # touser,title,content,from_user,status_id
        email_list = models.UserInfo.objects.filter(id__in=userinfo_list)
        print(email_list)

        print('ajax')
        # user_obj = models.UserInfo.objects.filter(id=delete_id).first()

        # print(user_obj,'用户呢')/

        touser = request.user
        print(touser, '发送人')
        title = request.POST.get("title")
        content = request.POST.get("content")
        ''' 邮箱不能再前端动态的获取因为是群发必须在循环里面取到'''
        from_user = request.POST.getlist("from_user")  # 邮箱
        # from_user1 = user_obj.user.email
        for i in email_list:
            allEmail.user_mail(request.user, title, content, i.user.email, 0)
        # user2=list(from_user)

        # user_id=delete_id
        # print(from_user, '邮箱邮箱邮箱有用喜爱那个')
        # status_id = request.POST.get("status_id")  # 默认未读
        # user_id = User.objects.filter(email=from_user[0]).values("id").first()
        # print(user_id)

        # Fhsms.objects.create(title=title, content=content, to_user=touser,
        #                          status_id_id=0, from_user=user_obj.user)
        # send_mail(subject=title, message=content, from_email=settings.EMAIL_FROM,
        #               recipient_list=user2)

        return JsonResponse({"status": True})
    return JsonResponse({"status": False})


''' 发送短信'''


def send_message(request):
    from user_management import message
    if request.method == 'POST':
        mobile = request.POST.get("mes_phone")

        mes_content = request.POST.get("mes_content")
        text = "您的验证码是：" + str(mes_content) + "。请不要把验证码泄露给其他人。 "

        message.send_sms(mobile, text)
        print('welcome new world')
    return redirect('/user_management/user_info/')


''' 群发信息'''


def group_sms(request):
    print('群发站信cccccccccccccccccccccccccccccc')
    from user_management import message
    if request.is_ajax():
        userinfo_list = request.POST.getlist("delete_id_list")
        user_list = models.UserInfo.objects.filter(id__in=userinfo_list)
        content = request.POST.get("content")
        for i in user_list:
            moble = i.user_phone
            message.send_sms(content, moble)
        return JsonResponse({"status": True})
    return JsonResponse({"status": False})


''' 舆情'''


def serach_emotion(request):
    return render(request, "user_management_html/search_emotion.html")


def erach_emotions(request):
    if request.method == "POST":
        search_key = request.POST.get("search_key")
        if search_key:
            system_list = models.System_setup.objects.filter(Scheme_name__icontains=search_key)
        return render(request, 'user_management_html/search_emotion.html', locals())


def add_emotion(request):
    return render(request, "user_management_html/add_emotion.html")


# def edit_emotion(request):
#     return render(request, "user_management_html/add_emotion.html")

def phone_management(request):
    return render(request, "user_management_html/phone_management.html")


# 通讯录信息
def mails(request):
    mails_list = models.Mail_list.objects.all()
    page = Page(mails_list, request, 10, 10)
    sum = page.Sum()
    return render(request, 'user_management_html/phone_management.html', {'mails_list': sum[0], 'page_html': sum[1]})


''' 添加通讯录 '''


def add_mail(request):
    print('czx')
    if request.method == "POST":
        mail_phone = request.POST.get('mail_phone')
        mail_name = request.POST.get('mail_name')
        mail_remarks = request.POST.get('mail_remarks')
        mail_email = request.POST.get('mail_email')
        mail_weixin_number = request.POST.get('mail_weixin_number')
        mail_company = request.POST.get('mail_company')

        Mail_list = models.Mail_list.objects.create(
            mail_phone=mail_phone,
            mail_name=mail_name,
            mail_remarks=mail_remarks,
            mail_email=mail_email,
            mail_weixin_number=mail_weixin_number,
            mail_company=mail_company,

        )

        return redirect("/user_management/mails/")
    return render(request, "user_management_html/phone_management.html", locals())


def delete_mail(request, num=None):
    if num:
        '''  对于删除先删除第三张表再删除作者表 id  注意页面的格式问题'''
        del_obj = models.Mail_list.objects.filter(id=num)

        del_obj.delete()
        return redirect('/user_management/mails/')
    if request.is_ajax():
        delete_id_list = request.POST.getlist("delete_id_list")
        for delete_id in delete_id_list:
            models.Mail_list.objects.filter(id=delete_id).delete()
        return JsonResponse({"status": True})
    return JsonResponse({"status": False})


def edit_mail(request, mail_id):
    print('welcome new  world')
    print(mail_id)
    if request.method == 'POST':
        mail_name = request.POST.get('mail_name')
        mail_phone = request.POST.get('mail_phone')
        mail_email = request.POST.get('mail_email')
        mail_weixin_number = request.POST.get('weixin_number')
        mail_remarks = request.POST.get('mail_remarks')
        mail_company = request.POST.get('mail_company')
        mailss = models.Mail_list.objects.filter(pk=mail_id)
        print(mailss)
        mailss.update(
            mail_phone=mail_phone,
            mail_name=mail_name,
            mail_email=mail_email,
            mail_weixin_number=mail_weixin_number,
            mail_remarks=mail_remarks,
            mail_company=mail_company

        )
        return redirect("/user_management/mails")

    return render(request, "user_management_html/phone_management.html", locals())


''' 精准问题反馈表'''


def problem_feedback(request):
    return render(request, "user_management_html/problem_feedback.html")


def serch_feedback(request):
    if request.method == "POST":
        search_key = request.POST.get("search_key")
        print(search_key)
        choice_title = request.POST.get("choice_title")
        if choice_title == "员工编号":
            staff_list = models.Staff.objects.filter(id__icontains=search_key)
        elif choice_title == "员工姓名":
            staff_list = models.Staff.objects.filter(staff_name__icontains=search_key)
        elif choice_title == "职位名称":
            staff_list = models.Staff.objects.filter(staff_job__icontains=search_key)
        elif choice_title == "职务级别":
            staff_list = models.Staff.objects.filter(staff_job_level__icontains=search_key)
    return render(request, 'employee_management/search_employee.html', locals())


''' 检查通讯录的手机号'''


@csrf_exempt
def check_mailphone(request):
    print('通讯录验证')
    data = {}
    print(request.is_ajax())

    if request.is_ajax():
        user_phone = request.POST.get("mail_phone", None)
        print(type(user_phone), user_phone)
        if len(user_phone) == 11:
            print('885555')
            user = models.Mail_list.objects.filter(mail_phone=user_phone).first()
            print('1111')
            if user:
                data["message"] = 1
            else:
                data["message"] = 0
            print(data["message"])
            return JsonResponse(data)
        else:
            data["message"] = 1

        return JsonResponse(data)


''' 预警设置'''


def System_setup(request):
    system_list = models.System_setup.objects.all()
    page = Page(system_list, request, 10, 10)
    sum = page.Sum()
    return render(request, 'user_management_html/emotion_info.html', {'system_list': sum[0], 'page_html': sum[1]})


def delete_system(request, num=None):
    print('删除啊')
    if num:
        '''  对于删除先删除第三张表再删除作者表 id  注意页面的格式问题'''
        del_obj = models.System_setup.objects.filter(id=num)

        del_obj.delete()

        return redirect('/user_management/System_setup/')


'''添加预警信息'''


def yujing(request):
    print('添加添加')
    if request.method == 'POST':
        Scheme_name = request.POST.get('rule_name')
        print(Scheme_name)
        source = request.POST.get('source_type')
        print(source)
        switch = request.POST.get('switch')

        print(switch)
        warningcontent = request.POST.get('contents')
        print(warningcontent)
        warning_mode = request.POST.get('type')

        print(warning_mode)
        Content = models.System_setup.objects.create(
            Scheme_name=Scheme_name,
            warning_type=source,
            switch=switch,
            warning_mode=warning_mode,
            warning_content=warningcontent,

        )

        return redirect("/user_management/System_setup")

    return render(request, "user_management_html/emotion_info.html", locals())


''' 修改预警信息'''


def edit_emotion(request, system_id):
    if request.method == 'POST':
        Scheme_name = request.POST.get('Scheme_name')
        warning_type = request.POST.get('warning_type')
        switch = request.POST.get('switch')
        warning_mode = request.POST.get('warning_mode')
        warning_content = request.POST.get('warning_content')
        emotion = models.System_setup.objects.filter(pk=system_id)
        print(emotion)
        emotion.update(
            Scheme_name=Scheme_name,
            warning_type=warning_type,
            switch=switch,
            warning_mode=warning_mode,
            warning_content=warning_content,

        )
        return redirect("/user_management/System_setup")

    return render(request, "user_management_html/emotion_info.html", locals())



def count_user(request):
    net_user_lists = Article.objects.filter(id__gt=0)
    affected_sum = 0
    art_sum = 0
    cre_time = []
    for i in net_user_lists:
        affected_sum += i.affected_count
        art_sum += i.source_id
        cre_time.append(i.create_time)
    times=Series([cre_time])
    print(type(times))
    art_sums=list(range(art_sum))
    affected_sums=list(range(affected_sum))


    '''
    name_attribute = ['NumberID','UserID','ModuleID','StartDate','EndDate','Frequent']
    writerCSV=pd.DataFrame(columns=name_attribute,data=data)
    test=pd.DataFrame(columns=name,data=list)
    writerCSV.to_csv('./no_fre.csv',encoding='utf-8')
    这种方法通过pandas模块的to_csv方法实现将二维的list转为csv，但是同样

    '''
    ''' 不能是data = [[art_sums],[affected_sums]] 因为art_sums 本身就是集合
        这样是错误的加上给列加上名字因为data里面的的集合有多少就要指明几列，这样显然是不对的
    '''
    # data = [art_sums,affected_sums]
    # name_attribute = ['art_sum','affected_sum']
    # writerCSV = pd.DataFrame( data=data)
    # writerCSV.to_csv('art_sums.csv', encoding='utf-8')



    # # s1 = Series([art_sums, affected_sums], index=['art_sums', 'affected_sums'])
    # s1 = Series([art_sums,affected_sums],index=None)
    # # s1 = Series([times], index=['times'])
    #
    # plt.title(u"文章影响率", fontproperties=font)
    # # 并转图 kind='pie', subplots=True
    # s1.plot(grid=True, label='s1',)
    # plt.xlabel('文章数', fontproperties=font)
    # plt.ylabel('受影响的人数', fontproperties=font)
    #
    # plt.legend()
    # # plt.savefig('xy标题标签')
    # plt.show()
    return HttpResponse(affected_sum)

def datacount(request):
    art_sums = pd.read_csv('art_sums.csv')
    # print(art_sums.head(2))
    # art_sums.head(2).plot(grid=True, title='alijd', label='alibaba', )
    # art_sums.plot(grid=True, title='alijd', label='alibaba',)
    art_sums['0'].plot(grid=True, title='alijd', label='alibaba', )
    plt.xlabel('文章数', fontproperties=font)
    plt.ylabel('受影响的人数', fontproperties=font)
    plt.legend()
    # plt.savefig('京东阿里')
    plt.show()
    return HttpResponse("hello  new  world")

