   $("#sendallmess").click(function () {

            var title = $('.titles').val()
            var content = $('.contents').val()

            var delete_id_list = [];
            $(".check_item").each(function () {
                if ($(this).prop("checked")) {
                    var delete_id = $(this).attr("delete_id");
                    delete_id_list.push(delete_id);
                }
            });
            $.ajax({
                url: "/user_management/all_email/",
                type: "post",
                traditional: true,
                data: {
                    "delete_id_list": delete_id_list,
                    'title': title,
                    'content': content,
                    "csrfmiddlewaretoken": "{{ csrf_token }}"
                },
                success: function (data) {

                    if (data.status)
                        alert('发送成功')
                    window.location.reload()
                }
            });


        });
