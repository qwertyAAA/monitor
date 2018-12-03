# Create your views here.
from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_exempt
from middlewares.all_requests import all_requests
from .Myutilss.pageutil import Page
from permission.models import Role
from mail.models import Fhsms

''' 发送站内信需要导入的包'''
from mail.models import Fhsms, StatusMail
from django.contrib.auth.models import User
from django.conf import settings
from django.core.mail import send_mail

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
    print('czx')

    if request.method == "POST":
        user_id = request.POST.get('user_id')
        user_name = request.POST.get('user_name')
        user_number = request.POST.get('adduser_number')
        user_id_card = request.POST.get('user_id_card')
        user_stay_years = request.POST.get('user_stay_years')
        user_gender = request.POST.get('user_gender')
        user_phone = request.POST.get('user_phone')
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
    user_list = models.UserInfo.objects.all()
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
    print(request.is_ajax())
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
    data = {}
    print(request.is_ajax())

    if request.is_ajax():
        user_phone = request.POST.get("user_phone", None)
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
    print(request.is_ajax())
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
        print(users)
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
                    all_requests.requests_user_pk.remove(request.user.pk)
                    logout(other_request)
    return JsonResponse({"status": True})


'''  单个下线'''


def online_users_delete(request, delete_id):
    print("WTF怎么不下线啊")
    for item in all_requests.requests_list:
        if item.user.pk == int(delete_id):
            all_requests.requests_list.remove(item)
            all_requests.requests_user_pk.remove(request.user.pk)
            logout(item)
    print(all_requests.requests_user_pk)
    return redirect("/user_management/online_users/")


def get_online_requests(request):
    return JsonResponse({"online_requests_count": len(all_requests.requests_list)})


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
        print(user_id["id"])
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
