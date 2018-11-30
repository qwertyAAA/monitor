from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password
from permission.models import Role
from django.contrib.auth.models import User
from django.contrib import auth
from permission.service.Permission import init_permission
from online_management.online_users import online_users


def login(request):
    if request.method == "POST":
        username = request.POST.get("username", None)
        password = request.POST.get("password", None)
        remember_pwd = request.POST.get("remember_pwd", None)
        print(remember_pwd, "****************")
        user = auth.authenticate(username=username, password=password)
        if user:
            auth.login(request, user)
            request.session['user_id'] = user.id
            init_permission(user, request)
            if remember_pwd:
                response = render(request, "index.html")
                response.set_cookie("username", username)
                response.set_cookie("password", password)
                return response
            else:
                return redirect("/index/")
        else:
            message = "账号或密码错误，请重新输入！"
            return render(request, "login.html", locals())
    else:
        try:
            username = request.COOKIES.get("username")
            print(username)
            password = request.COOKIES.get("password")
            user = auth.authenticate(username=username, password=password)
            print(user)
            if user:
                auth.login(request, user)
                return redirect("/index/")
            else:
                return render(request, "login.html")
        except:
            return render(request, "login.html")


def register(request):
    js_code = """
        window.onload = function(){
        $('#login-box').removeClass('visible');
        $('#signup-box').addClass('visible');
        }            
    """
    if request.method == "POST":
        username = request.POST.get("username", None)
        password = request.POST.get("password", None)
        email = request.POST.get("email", None)
        user = User.objects.filter(email=email)
        user2 = User.objects.filter(username=username)
        if user:
            reg_result = "该邮箱已注册，请直接登录！"
            return render(request, "login.html", locals())
        elif user2:
            reg_result = "该用户名已注册，请换个用户名！"
            return render(request, "login.html", locals())

        # 添加到数据库
        user = User.objects.create_user(username=username, password=password, email=email)

        # 调用auth登录
        auth.login(request, user)
        # 重定向到首页
        return redirect("/index/")
    else:
        context = {"islogin": False}
    return render(request, "login.html", locals())


def logout(request):
    print(request.META["HTTP_REFERER"])
    try:
        auth.logout(request)
    except Exception as e:
        print(e)
    return redirect(request.META['HTTP_REFERER'])


def forget_pwd(request):
    pass


def index(request):
    return render(request, "index.html")


def check_email(request):
    data = {}
    if request.is_ajax():
        if request.method == "POST":
            email = request.POST.get("email", None)
            user = User.objects.filter(email=email)
            if user:
                data["message"] = 1
            else:
                data["message"] = 0
    return JsonResponse(data)


def check_username(request):
    data = {}
    if request.is_ajax():
        if request.method == "POST":
            username = request.POST.get("username", None)
            user = User.objects.filter(username=username)
            if user:
                data["message"] = 1
            else:
                data["message"] = 0
    return JsonResponse(data)
