  $.ajaxSetup({
            data: {csrfmiddlewaretoken: '{{ csrf_token }}'},
        });

        $('body').delegate('#adduser_number', 'blur', function () {
            var user_id_card = $("#user_id_card").val();
            if (user_id_card != "") {

                $.post(
                    "/user_management/check_usernumber/",
                    {
                        "user_id_card": user_id_card
                    },
                    function (data) {
                        console.log(data.message);
                        if (data.message == 1) {

                            $("#message").text("手机号已被占用或者不是十一位");



                        }
                        else {
                            <!-- $('#message').css('display','none'); 不能这样设置 当第二次判断的时候 即使是错的的也无法进行错误提示显示  -->
                            $("#message").text("");

                        }
                    }
                )
            }
        });
