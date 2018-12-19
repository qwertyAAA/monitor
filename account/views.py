from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib import auth
from permission.service.Permission import init_permission
from middlewares.all_requests import all_requests
from django.contrib.auth.hashers import make_password
from mail.models import Fhsms


# 登录
def login(request):
    data = {}
    if request.method == "POST":
        username = request.POST.get("username", None)
        print(username)
        password = request.POST.get("password", None)
        print(password)
        valid_code = request.POST.get("valid_code", None)
        remember_pwd = request.POST.get("remember_pwd", None)
        user = auth.authenticate(username=username, password=password)
        print(user, "************")
        if valid_code.upper() == request.session.get("valid_code", "").upper():
            if user:
                auth.login(request, user)
                request.session['user_id'] = user.id
                init_permission(user, request)
                data["success"] = 1
                if remember_pwd:
                    request.session.set_expiry(None)
                else:
                    request.session.set_expiry(0)
            else:
                login_message = "账号或密码错误，请重新输入！"
                data["login_message"] = login_message
        else:
            login_message = "验证码错误！"
            data["login_message"] = login_message
        return JsonResponse(data)
    else:
        return render(request, "login.html")


# 注册
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
        return redirect("/index/spider_message/")
    else:
        context = {"islogin": False}
    return render(request, "login.html", locals())


# 注销
def logout(request):
    print(request.META["HTTP_REFERER"])
    try:
        for obj in all_requests.requests_list:
            if obj.user.pk == request.user.pk:
                all_requests.requests_list.remove(obj)
                all_requests.requests_user_pk.remove(obj.user.pk)
        auth.logout(request)
    except Exception as e:
        print(e)
    return redirect("/login/")


# 重置密码
def reset_pwd(request):
    if request.method == "POST":
        data = {}
        newPwd = make_password(request.POST.get("newPwd", None))
        auth_id = request.session["auth_id"]
        if newPwd:
            User.objects.filter(id=auth_id).update(password=newPwd)
            data["message"] = 1
            return JsonResponse(data)
        else:
            data["message"] = 0
            return JsonResponse(data)


# 首页
def index(request):
    return render(request, "index.html")


# Ajax验证邮箱是否注册
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


# Ajax验证用户名是否已注册
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


# 发送邮件验证码
def sendEmail(request):
    message = {}
    message["result"] = None
    print(request.method, "************")
    # 第一次发送邮箱验证码的请求方法为POST，重新发送为GET
    if request.method == "POST":
        emailaddress = request.POST.get("email_find", None)
        print(emailaddress)
        if User.objects.filter(email=emailaddress):
            email_sender(request, emailaddress, message)
            if message["result"] == False:
                message["send_result"] = 0
                message["failed"] = "邮件发送异常，请稍后再试！"
                # return render(request, "login.html", locals())
                return JsonResponse(message)
            message["send_result"] = 1
            # return render(request, "login.html", locals())
            return JsonResponse(message)
        else:
            message["failed"] = "您的邮箱的账户注册信息没有找到"
            js_code = """
                        window.onload = function(){
                        $('#login-box').removeClass('visible');
                        $('#forgot-box').addClass('visible');
                        $("#no_email").text(data["failed"]);
                        $("#send_emailAdress").css("disabled", false);
                        }            
                    """
            return render(request, "login.html", locals())
    # 前端把重新发送验证码的请求设置为GET
    elif request.method == "GET":
        emailaddress = request.GET.get("email_find", None)
        email_sender(request, emailaddress, message)
        if message["result"] == False:
            js_code = """
                        window.onload = function(){
                        $('#login-box').removeClass('visible');
                        $('#forgot-box').addClass('visible');
                        $("#no_email").text(data["failed"]);
                        $("#send_emailAdress").css("disabled", false);
                        }            
                    """
            message["failed"] = "邮件发送异常，请稍后再试！"
            return render(request, "login.html", locals())
        js_code = """
                    window.onload = function(){
                    $('#login-box').removeClass('visible');
                    $('#emailCode-box').addClass('visible');
                    $("#email_status").text(data["success"]);
                    }            
                """
        return render(request, "login.html", locals())


# 定义发送邮件的方法
def email_sender(request, emailaddress, message):
    for i in User.objects.filter(email=emailaddress):
        nametemp = i.username
        idtemp = i.id
        # 生成随机验证码
        from random import choice
        import string
        # python3中为string.ascii_letters,而python2下则可以使用string.letters和string.ascii_letters
        def GenPassword(length=8, chars=string.ascii_letters + string.digits):
            return ''.join([choice(chars) for i in range(length)])

        pawdtemp = GenPassword(8)

        import smtplib
        from email.mime.text import MIMEText
        host = "smtp.163.com"
        port = 25
        sender = "codelegend@163.com"
        pwd = "xiaoyang789"
        receiver = emailaddress
        # body = "<h1>您本次重置密码的验证码是：  " + pawdtemp + "  ，请尽快操作！</h1>"
        body = pawdtemp
        msg = MIMEText(body, "html")
        msg["subject"] = "来自老朋友的问候"
        msg["from"] = sender
        msg["to"] = receiver
        print(msg["to"])

        try:
            s = smtplib.SMTP(host, port)
            s.login(sender, pwd)
            s.sendmail(sender, receiver, msg.as_string())
            print("邮件发送成功！")
            request.session["findBy_email"] = emailaddress
            request.session["email_code"] = pawdtemp
            request.session["auth_id"] = idtemp
            message["success"] = "验证码已经发送到您的邮箱，请尽快登录邮箱以完成密码更新！"
            print(request.session["email_code"])
        except smtplib.SMTPException as e:
            print(e)
            message["result"] = False
            message["failed"] = "服务器异常，请重试"


# 校验邮箱验证码
def check_code(request):
    data = {}
    if request.method == "GET":
        email_code = request.GET.get("email_code", None)
        if email_code.upper() == request.session["email_code"].upper():
            data["result"] = 1
        else:
            data["result"] = 0
        return JsonResponse(data)


# 登录验证码生成
def get_valid_img(request):
    # with open("valid_code.png", "rb") as f:
    #     data = f.read()
    # 自己生成一个图片
    from PIL import Image, ImageDraw, ImageFont
    import random

    # 获取随机颜色的函数
    def get_random_color():
        return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)

    # 生成一个图片对象
    img_obj = Image.new(
        'RGB',
        (220, 35),
        get_random_color()
    )
    # 在生成的图片上写字符
    # 生成一个图片画笔对象
    draw_obj = ImageDraw.Draw(img_obj)
    # 加载字体文件， 得到一个字体对象
    font_obj = ImageFont.truetype("/static/fonts/arial.ttf", 28)
    # 开始生成随机字符串并且写到图片上
    tmp_list = []
    for i in range(5):
        u = chr(random.randint(65, 90))  # 生成大写字母
        l = chr(random.randint(97, 122))  # 生成小写字母
        n = str(random.randint(2, 9))  # 生成数字，注意要转换成字符串类型

        tmp = random.choice([u, l, n])
        tmp_list.append(tmp)
        draw_obj.text((20 + 40 * i, 0), tmp, fill=get_random_color(), font=font_obj)

    print("".join(tmp_list))
    print("生成的验证码".center(120, "="))
    # 不能保存到全局变量
    # global VALID_CODE
    # VALID_CODE = "".join(tmp_list)

    # 保存到session
    request.session["valid_code"] = "".join(tmp_list)
    # 加干扰线
    # width = 220  # 图片宽度（防止越界）
    # height = 35
    # for i in range(5):
    #     x1 = random.randint(0, width)
    #     x2 = random.randint(0, width)
    #     y1 = random.randint(0, height)
    #     y2 = random.randint(0, height)
    #     draw_obj.line((x1, y1, x2, y2), fill=get_random_color())
    #
    # # 加干扰点
    # for i in range(40):
    #     draw_obj.point((random.randint(0, width), random.randint(0, height)), fill=get_random_color())
    #     x = random.randint(0, width)
    #     y = random.randint(0, height)
    #     draw_obj.arc((x, y, x+4, y+4), 0, 90, fill=get_random_color())

    # 将生成的图片保存在磁盘上
    # with open("s10.png", "wb") as f:
    #     img_obj.save(f, "png")
    # # 把刚才生成的图片返回给页面
    # with open("s10.png", "rb") as f:
    #     data = f.read()

    # 不需要在硬盘上保存文件，直接在内存中加载就可以
    from io import BytesIO
    io_obj = BytesIO()
    # 将生成的图片数据保存在io对象中
    img_obj.save(io_obj, "png")
    # 从io对象里面取上一步保存的数据
    data = io_obj.getvalue()
    return HttpResponse(data)
