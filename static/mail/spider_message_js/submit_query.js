// 列表信息查询的ajax
$("#submit_query").click(function () {
    var click_val = $(".click");
    // console.log(arr_click_id);
    var arr_click = [];
    click_val.each(function () {
        arr_click.push($(this).text());
        // console.log($(this).text())
    });
    // console.log(arr_click);
    $.ajax({
        url: '/index/submit_query/',
        data: {
            'arr_click': arr_click,
            'csrfmiddlewaretoken': $("[name='csrfmiddlewaretoken']").val(),
        },
        type: 'post',
        dataType: 'json',
        traditional: true,
        success: function (data) {
            var new_data = JSON.parse(data);
            // console.log(data);
            var new_tr = "";
            $('tbody').empty();
            $.each(new_data, function (item) {
                console.log(typeof $(this.fields.title));
                console.log($(this.fields.create_time));
                new_tr += "<tr>" +
                    "<td class='input_checkbox line_height'>" +
                    "<input type='checkbox' id='onclick_checkbox' name='onclick_checkbox' value='" + $(this.pk) + "'>" +
                    '</td>' +
                    '<td>' +
                    '<div class="tr_content" style="font-size:14px;">' +
                    '<a href="/index/' + $(this.fields.title) + '/article/id=' + $(this.pk) + '/">' +
                    '<img src="/media/' + $(this.fields.source) + '" class="img-circle" style="width:50px;height:50px;">' +
                    '</a>' +
                    '<a href="/index/' + $(this.fields.title) + '/article/id=' + $(this.pk) + '/">' +
                    '<span>' + $(this.fields.title) + '</span>' +
                    '</a><br>' +
                    '<span class="content_50">' + $(this.fields.detail) + '</span><br>' +
                    '<span>' + "涉及词：" + $(this.fields.keywords) + '</span><br>' +
                    '<div class="one_button" style="float:right">' +
                    '<button type="button" class="btn" data-toggle="tooltip" data-placement="bottom" id="in_heart_one" name="in_heart_one" title="加入收藏夹" value="' + $(this.pk) + '" >' +
                    '<i class="fa fa-heart" aria-hidden="true"></i>' +
                    '</button>' +
                    '<button type="button" class="btn" data-toggle="tooltip" data-placement="bottom" id="in_tags_one" name="in_tags" data-original-title="加入简报素材" >' +
                    '<i class="fa fa-tags" aria-hidden="true"></i>' +
                    '</button>' +
                    '<button type="button" class="btn" data-toggle="tooltip" data-placement="bottom" name="in_square" data-original-title="转发舆情" >' +
                    '<i class="fa fa-share-square-o" aria-hidden="true"></i>' +
                    '<i class="fa fa-angle-down" aria-hidden="true"></i>' +
                    '</button>' +
                    '<button type="button" class="btn" data-toggle="tooltip" data-placement="bottom" name="out_del_one" data-original-title="删除" >' +
                    '<i class="fa fa-trash-o fa-lg"></i>' +
                    '</button>' +
                    '<a href="' + $(this.fields.url) + '">' +
                    '<button type="button" class="btn" data-toggle="tooltip" data-placement="bottom" data-original-title="查看原文">' +
                    '<i class="fa fa-link fa-lg"></i>' +
                    '</button>' +
                    // 判断语句********************************
                    '<button type="button" class="btn" data-toggle="tooltip" data-placement="bottom" name="in_eye" data-original-title="标已读" >' +
                    '<i class="fa fa-eye-slash" aria-hidden="true"></i>' +
                    '</button>' +
                    // ************************************
                    '</div>' + '</div>' + '</td>' +
                    '<td class="line_height"><span>' + 1 + '</span></td>' +
                    '<td class="line_height"><span>' + $(this.fields.source.source) + '</span></td>' +
                    '<td class="line_height"><span>' + $(this.fields.create_time) + '</span></td>' +
                    '</tr>';
                $('tbody').html(new_tr);
            })
            // window.location.reload();
        },
        error: function (data) {
            alert("未知错误！！！")
        }
    })
});