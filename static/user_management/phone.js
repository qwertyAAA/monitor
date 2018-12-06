$.ajaxSetup({
    data: {csrfmiddlewaretoken: '{{ csrf_token }}'},
});

$('body').delegate('#ckuser_phone', 'blur', function () {
    var ckuser_phone_var = $("#ckuser_phone").val();
    if (ckuser_phone_var != "") {

        $.post(
            "/user_management/check_userphone/",
            {
                "ckuser_phone": ckuser_phone_var
            },
            function (data) {
                console.log(data.message);
                if (data.message == 1) {

                    $("#phonemessage").text("手机号已被占用或者不是十一位");
                    $('#save').addClass("disabled");


                }
                else {
                    <!-- $('#message').css('display','none'); 不能这样设置 当第二次判断的时候 即使是错的的也无法进行错误提示显示  -->
                    $("#phonemessage").text("");
                    $('#save').removeClass("disabled");

                }
            }
        )
    }
});
