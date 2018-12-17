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
            // console.log(data);
            $('tbody').empty();
            var new_tr = "";
            $.each(data, function (item) {
                var new_btn = "";
                var new_read = "";
                // console.log(this.status);
                if (this.status === false){
                    new_btn = '<button style="background-color: #f1d153;color: black">'+ "非敏感" +'</button><br>'
                }
                else {
                    new_btn = '<button style="background-color: red;color: black">'+ "敏感" +'</button><br>'
                }
                if (this.already_read === false){
                    new_read = '<button type="button" class="btn" data-toggle="tooltip" data-placement="bottom" name="in_eye" data-original-title="标已读">' +
                        '<i class="fa fa-eye-slash" aria-hidden="true"></i>' +
                        '</button>'
                }
                else {
                    new_read = '<button type="button" class="btn" data-toggle="tooltip" data-placement="bottom" name="in_eye" data-original-title="已读" style="background-color: #f1d153">' +
                        '<i class="fa fa-eye" aria-hidden="true"></i>' +
                        '</button>'
                }
                if (item < 10) {
                    new_tr += "<tr>" +
                        "<td class='input_checkbox line_height'>" +
                        "<input type='checkbox' id='onclick_checkbox' name='onclick_checkbox' value='" + this.id + "'>" +
                        '</td>' +
                        '<td>' +
                        '<div class="tr_content" style="font-size:14px;">' +
                        '<a href="/index/' + this.title + '/article/id=' + this.id + '/">' +
                        '<img src="/media/' + this.source_img + '" class="img-circle" style="width:50px;height:50px;">' +
                        '</a>' +
                        '<a href="/index/' + this.title + '/article/id=' + this.id + '/">' +
                        '<span>' + this.title + '</span>' +
                        '</a>' + new_btn +
                        '<span class="content_50">' + this.detail + '</span><br>' +
                        '<span>' + "涉及词：" + this.keywords + '</span><br>' +
                        '<div class="one_button" style="float:right">' +
                        '<button type="button" class="btn" data-toggle="tooltip" data-placement="bottom" id="in_heart_one" name="in_heart_one" title="加入收藏夹" value="' + this.id + '" >' +
                        '<i class="fa fa-heart" aria-hidden="true"></i>' +
                        '</button>' +
                        '<button type="button" class="btn" data-toggle="tooltip" data-placement="bottom" id="in_tags_one" name="in_tags" data-original-title="加入简报素材">' +
                        '<i class="fa fa-tags" aria-hidden="true"></i>' +
                        '</button>' +
                        '<button type="button" class="btn" data-toggle="tooltip" data-placement="bottom" name="in_square" data-original-title="转发舆情" >' +
                        '<i class="fa fa-share-square-o" aria-hidden="true"></i>' +
                        '<i class="fa fa-angle-down" aria-hidden="true"></i>' +
                        '</button>' +
                        '<button type="button" class="btn" data-toggle="tooltip" data-placement="bottom" name="out_del_one" data-original-title="删除">' +
                        '<i class="fa fa-trash-o fa-lg"></i>' +
                        '</button>' +
                        '<a href="' + this.url + '">' +
                        '<button type="button" class="btn" data-toggle="tooltip" data-placement="bottom" data-original-title="查看原文">' +
                        '<i class="fa fa-link fa-lg"></i>' +
                        '</button>' +
                        // 判断语句********************************
                        new_read +
                        // ************************************
                        '</div>' + '</div>' + '</td>' +
                        '<td class="line_height"><span>' + 1 + '</span></td>' +
                        '<td class="line_height"><span>' + this.source + '</span></td>' +
                        '<td class="line_height"><span>' + this.create_time + '</span></td>' +
                        '</tr>';
                }
                else {
                    return false;
                }
            });
            $('tbody').append(new_tr);
            // window.location.reload();
        },
        error: function (data) {
            alert("未知错误！！！或部分查询信息二期完成")
        }
    })
});
// 列表模糊搜索
$("#obang").click(function () {
    var obang = $("#obang_input").val();
    $("table .old_tbody").html("");
    var csrfToken = $("[name='csrfmiddlewaretoken']").val();
    $.ajax({
        url: "/index/obang_new_tbody/",
        type: "post",
        data: {
            "obang": obang,
            "csrfmiddlewaretoken": csrfToken,
        },
        success: function (data) {
            if (data.status) {
                $(".table .old_tbody").append(data.html)
            }
            else {
                alert("出现了未知错误！")
            }
        },
        error: function () {
            alert("error")
        }
    });
});
