from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib import auth


def login(request):
    context = {}
    if request.method == "POST":
        username = request.POST.get("username", None)
        password = request.POST.get("password", None)
        user = auth.authenticate(username=username, password=password)
        if user:
            auth.login(request, user)
            return redirect("/index/")
        else:
            context = {
                "islogin": False,
                "pwd": False
            }
            return render(request, "login.html", context)
    else:
        context = {
            "islogin": False,
            "pwd": True
        }
    return render(request, "login.html", context)


def register(request):
    context = {}
    if request.method == "POST":
        username = request.POST.get("username", None)
        password = request.POST.get("password", None)
        email = request.POST.get("email", None)
        # 判断用户是否存在
        user = auth.authenticate(username=username, password=password)
        if user:
            context["userExit"] = True
            return redirect("/login/")

        # 添加到数据库
        user = User.objects.create_user(username=username, password=password, email=email)
        user.save()

        # 调用auth登录
        auth.login(request, user)
        # 重定向到首页
        return redirect("/index/")
    else:
        context = {"islogin": False}
    return render(request, "login.html", context)


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
