$("#send_allmess").click(function () {


    var text = $('.allsms').val()

    var delete_id_list = [];

    $(".check_item").each(function () {
        if ($(this).prop("checked")) {
            var delete_id = $(this).attr("delete_id");
            delete_id_list.push(delete_id);
        }
    });

    $.ajax({
        url: "/user_management/group_sms/",
        type: "post",
        traditional: true,
        data: {
            "delete_id_list": delete_id_list,
            'text': text,
            // 在js单独写文件ajax的时候必须这么来取csrf  因为字节取是娶不到的
            "csrfmiddlewaretoken": $("#csrf").text()
        },

        success: function (data) {

            if (data.status) {
                alert('发送成功')
                window.location.reload()
            }

        }
    });


});
