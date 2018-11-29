jQuery(function ($) {
    $(document).on('click', '.toolbar a[data-target]', function (e) {
        e.preventDefault();
        var target = $(this).data('target');
        $('.widget-box.visible').removeClass('visible');//hide others
        $(target).addClass('visible');//show target
    });
});


//you don't need this, just used for changing background
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

//CSRF设置
$.ajaxSetup({
    data: {csrfmiddlewaretoken: '{{ csrf_token }}'},
});
//邮箱Ajax查重
$("#email").blur(function () {
    var email_val = $("#email").val();
    if (email_val != "") {
        $.post(
            "/account/check_email/",
            {
                "email": $("#email").val()
            },
            function (data) {
                if (data["message"] == 1) {
                    $("#message").text("该邮箱已注册！");
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
            },
            function (data) {
                if (data["message"] == 1) {
                    $("#message").text("该用户名已被注册！");
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
$(document).on('focus', '#login_username, #login_pwd', function () {
    $("#login_result").text("");
});

//判断登录信息为空
function validateForm() {
    var username = $("#login_username").val();
    var password = $("#login_pwd").val();
    if (username == "" || username == null || password == "" || password == null) {
        $("#login_result").text("账号和密码不能为空！");
        return false;
    }
    return true;
}

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

    if (email == null || email == "" || username == null || username == "" || pwd == null || pwd == "") {
        $("#message").text("注册信息不完整！");
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