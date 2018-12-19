csrf_val = $("#csrf_val").text();
//login页面的注册、登录、忘记密码模块切换
jQuery(function ($) {
    $(document).on('click', '.toolbar a[data-target]', function (e) {
        e.preventDefault();
        var target = $(this).data('target');
        $('.widget-box.visible').removeClass('visible');//hide others
        $(target).addClass('visible');//show target
    });
});


//you don't need this, just used for changing background
// 背景切换
jQuery(function ($) {
    $('#btn-login-dark').on('click', function (e) {
        $('body').attr('class', 'login-layout');
        $('#id-text2').attr('class', 'white');
        $('#id-company-text').attr('class', 'blue');

        e.preventDefault();
    });
    $('#btn-login-light').on('click', function (e) {
        $('body').attr('class', 'login-layout light-login');
        $('#id-text2').attr('class', 'grey');
        $('#id-company-text').attr('class', 'blue');

        e.preventDefault();
    });
    $('#btn-login-blur').on('click', function (e) {
        $('body').attr('class', 'login-layout blur-login');
        $('#id-text2').attr('class', 'white');
        $('#id-company-text').attr('class', 'light-blue');

        e.preventDefault();
    });

});

// 点击验证码图片 刷新验证码
$("#valid-img").click(function () {
    $(this)[0].src += "?";
});


//判断是否接受协议
$("#protocol").change(function () {
    if ($("#protocol").is(":checked") == true) {
        $("#register").attr("disabled", false);
    } else {
        $("#register").attr("disabled", true);
    }
});
//判断两次密码是否一致
$("#password2").blur(function () {
    var p1 = $("#password").val();
    var p2 = $("#password2").val();
    if (p1 != p2) {
        $("#message").text("两次密码不一致！");
        $("#register").attr("disabled", true);
    } else {
        $("#message").text("");
        if ($("#protocol").is(":checked") == true) {
            $("#register").attr("disabled", false);
        }
    }
});
//重置
$("#reset").click(function () {
    $("#email").val("");
    $("#username").val("");
    $("#password").val("");
    $("#password2").val("");
    $("#message").text("");
});


//CSRF设置--js文件里不能用{{ csrf_token }}
$.ajaxSetup({
    data: {csrfmiddlewaretoken: csrf_val}
});
//邮箱Ajax查重
$("#email").blur(function () {
    var email_val = $("#email").val();
    if (email_val != "") {
        $.post(
            "/account/check_email/",
            {
                "email": $("#email").val()
                //"csrfmiddlewaretoken": csrf_val
            },
            function (data) {
                if (data["message"] == 1) {
                    $("#message").text("该邮箱已注册！");
                    $("#register").addClass("disabled");
                } else {
                    $("#register").removeClass("disabled");
                }
            }
        )
    }
});
//用户名Ajax查重
$("#username").blur(function () {
    var username_var = $("#username").val();
    if (username_var != "") {
        $.post(
            "/account/check_username/",
            {
                "username": username_var
                //"csrfmiddlewaretoken": csrf_val
            },
            function (data) {
                if (data["message"] == 1) {
                    $("#message").text("该用户名已被注册！");
                    $("#register").addClass("disabled");
                } else {
                    $("#register").removeClass("disabled");
                }
            }
        )
    }
});
//清除注册提示
$(document).on('focus', '#email, #username, #password, #password2', function () {
    $("#message").text("");
});
//清除登录提示
$(document).on('focus', '#login_username, #login_pwd, #valid_code', function () {
    $("#login_result").text("");
});
//清除发送邮件页面的异常提示
$(document).on('focus', '#emailAdress', function () {
    $("#no_email").text("");
});
//清除输入验证码页面的失败提示
$(document).on('focus', '#email_code', function () {
    $("#check_message").text("");
});
//清除输入验证码页面的失败提示
$(document).on('focus', '#newPwd, #newPwd2', function () {
    $("#reset_message").text("");
});


//登录Ajax
$("#btn-login").click(function () {
    var username = $("#login_username").val();
    var password = $("#login_pwd").val();
    var valid_code = $("#valid_code").val();
    var remember_pwd = $("#remenber_pwd").val();
    if (username == "" || username == null || password == "" || password == null || valid_code == "" || valid_code == null) {
        $("#login_result").text("账号、密码、验证码不能为空！");
    } else {
        $.post(
            "/login/",
            {
                "username": username,
                "password": password,
                "valid_code": valid_code,
                "remember_pwd": remember_pwd,
                "csrfmiddlewaretoken": csrf_val
            },
            function (data) {
                if (data["success"] == 1) {
                    $('#login-box').removeClass('visible');
                    $('#loginSuccess-box').addClass('visible');
                    var i = 3;
                    var intervalid;

                    function refer() {
                        if (i == 0) {
                            window.location.replace("/index/spider_message/");
                            clearInterval(intervalid);
                        }
                        $("#ls3s").text(i);
                        i--;
                    }

                    intervalid = setInterval(refer, 1000);
                } else {
                    $("#login_result").text(data["login_message"]);
                }
            }
        );

    }
});


//判断注册完整性和有效性
function check_reg() {
    var email = $("#email").val();
    var username = $("#username").val();
    var pwd = $("#password").val();
    var pwd2 = $("#password2").val();
    //验证用户名格式
    var regEn = /[`~!@#$%^&*()_+<>?:"{},.\/;'[\]]/;
    var regCn = /[·！#￥（——）：；“”‘、，|《。》？、【】[\]]/;
    //验证密码格式
    var pwd_reg = /^[0-9a-zA-Z_]{6,20}$/;
    //验证邮箱格式
    var email_reg = /^([a-zA-Z]|[0-9])(\w|\-)+@[a-zA-Z0-9]+\.([a-zA-Z]{2,4})$/;

    if (email == null || email == "" || username == null || username == "" || pwd == null || pwd == "") {
        $("#message").text("注册信息不完整！");
        return false;
    } else if (!email_reg.test(email)) {
        $("#message").text("邮箱格式不正确！");
        return false;
    } else if (pwd != pwd2) {
        $("#message").text("输入的密码不一致，请重新输入！");
        return false;
    } else if (regEn.test(username) || regCn.test(username) || username.length >= 21) {
        $("#message").text("用户名须少于20位且不含特殊字符！");
        return false;
    } else if (!pwd_reg.test(pwd)) {
        $("#message").text("密码只能是6-20位的字母、数字、下划线！");
        return false;
    }
}

//输入邮箱地址获取验证码
$("#send_emailAdress").click(function () {
    var email_find = $("#emailAdress").val();
    $.post(
        "/account/send_email/",
        {
            "email_find": email_find
        },
        function (message) {
            if (message["send_result"] == 1) {
                $('#forgot-box').removeClass('visible');
                $('#emailCode-box').addClass('visible');

                var i = 60;
                var intervalid;
                $("#reSend").addClass("disabled");

                function refer() {
                    if (i == 0) {
                        $("#reSend").removeClass("disabled");
                        clearInterval(intervalid);
                        $("#60s").text("重新发送");
                    } else {
                        $("#60s").text(i + "s");
                    }
                    i--;
                }

                intervalid = setInterval(refer, 1000);
            } else if (message["send_result"] == 0) {
                $("#no_email").text(message["failed"]);

                var i = 60;
                var intervalid;
                $("#send_emailAdress").addClass("disabled");

                function refer() {
                    if (i == 0) {
                        $("#send_emailAdress").removeClass("disabled");
                        clearInterval(intervalid);
                        $("#sentIt").text("发送!");
                    } else {
                        $("#sentIt").text(i + "s");
                    }
                    i--;
                }

                intervalid = setInterval(refer, 1000);
            }
        }
    )
});

//重新发送邮箱验证码
$("#reSend").click(function () {
    //var findBy_email = $("#findBy_email").text();
    var findBy_email = $("#emailAdress").val();
    $.get(
        "/account/send_email/?email_find=" + findBy_email,
        function (data) {
            var i = 60;
            var intervalid;
            $("#reSend").addClass("disabled");

            function refer() {
                if (i == 0) {
                    $("#reSend").removeClass("disabled");
                    clearInterval(intervalid);
                    $("#60s").text("重新发送");
                } else {
                    $("#60s").text(i + "s");
                }
                i--;
            }

            intervalid = setInterval(refer, 1000);
        }
    )
});

//邮箱验证码匹配验证
$("#check_code").click(function () {
    var email_code = $("#email_code").val();
    if (email_code != "" || email_code != null) {
        $.get(
            "/account/check_code/?email_code=" + email_code,
            function (data) {
                if (data["result"] == 1) {
                    $('#emailCode-box').removeClass('visible');
                    $('#resetPassword-box').addClass('visible');
                } else {
                    $("#check_message").text("验证失败，请检查输入是否正确或重新发送验证邮件！");
                }
            }
        );
    }
});

//重置密码：一致性验证和Ajax提交
$("#reset_pwd").click(function () {
    newPwd = $("#newPwd").val();
    newPwd2 = $("#newPwd2").val();
    //验证密码格式
    var pwd_reg = /^[0-9a-zA-Z_]{6,20}$/;
    if (newPwd == "" || newPwd == null) {
        $("#reset_message").text("密码不能为空！");
    }
    else if (newPwd != newPwd2) {
        $("#reset_message").text("两次密码不一致，请重新输入！");
    } else if (!pwd_reg.test(newPwd)) {
        $("#reset_message").text("密码只能是6-20位的字母、数字、下划线！");
    } else {
        $.post(
            "/account/reset_pwd/",
            {
                "newPwd": newPwd
                //"csrfmiddlewaretoken": csrf_val
            },
            function (data) {
                if (data["message"] == 1) {
                    var i = 3;
                    var intervalid;
                    $('#resetPassword-box').removeClass('visible');
                    $('#resetSuccess-box').addClass('visible');

                    function refer() {
                        if (i == 0) {
                            window.location.replace("/login/");
                            clearInterval(intervalid);
                        }
                        document.getElementById("ss").innerHTML = i;
                        i--;
                    }

                    intervalid = setInterval(refer, 1000);
                } else if (data["message"] == 0) {
                    $("reset_message").text("密码重置失败，请重试！");
                }
            }
        );
    }
});


