  $.ajaxSetup({
            data: {csrfmiddlewaretoken: '{{ csrf_token }}'},
        });

        $('body').delegate('#ckuser_id_card', 'blur', function () {
            var user_id_card = $("#ckuser_id_card").val();
            if (user_id_card != "") {

                $.post(
                    "/user_management/check_usercard/",
                    {
                        "user_id_card": user_id_card
                    },
                    function (data) {
                        console.log(data.message);
                        if (data.message == 1) {

                            $("#cardmessage").text("请检查您输入的身份证号");
                            $('#save').addClass("disabled");



                        }
                        else {
                            <!-- $('#message').css('display','none'); 不能这样设置 当第二次判断的时候 即使是错的的也无法进行错误提示显示  -->
                            $("#cardmessage").text("");
                              $('#save').removeClass("disabled");

                        }
                    }
                )
            }
        });
