$("#checkbox_on").click(function () {
    // 判断是否已全部选中
    if ($("input[type='checkbox']").is(':checked')) {
        // 如果没有全部选中或已全选，点击则取消已选择的checkbox
        $("input[name='onclick_checkbox']:checkbox").each(function () {
            $(this).prop("checked", false);
        });
    } else {
        // 如果都没有选中的话，点击则全部选上
        $("input[name='onclick_checkbox']:checkbox").each(function () {
            $(this).prop("checked", true);
        });
    }
});

//Ajax多选删除
$("#out_del").click(function () {
    var check_obj = document.getElementsByName("onclick_checkbox");
    var check_val = [];
    for (k in check_obj) {
        if (check_obj[k].checked)
            check_val.push(check_obj[k].value);
    }
    console.log(check_val);
    if ($("input[type='checkbox']").is(':checked')) {
        $.ajax({
            url: '/index/spider_del_all/',
            data: {'check_val': check_val,'csrfmiddlewaretoken':$("[name='csrfmiddlewaretoken']").val()},
            type: "post",
            dateType: "json",
            traditional: true,
            success: function (data) {
                alert("删除成功");
                window.location.reload();
            },
            error: function (data) {
                alert("出现错误！！！")
            }
        })
    }
    else {
        alert("没有被选中")
    }
});
// 多选加入收藏
$("#in_heart").click(function () {
    var check_obj = document.getElementsByName("onclick_checkbox");
    var check_val = [];
    for (k in check_obj) {
        if (check_obj[k].checked)
            check_val.push(check_obj[k].value);
    }
    console.log(check_val);
    if ($("input[type='checkbox']").is(':checked')) {
        $.ajax({
            url: '/index/spider_add_heart_all/',
            data: {'check_val': check_val,'csrfmiddlewaretoken':$("[name='csrfmiddlewaretoken']").val()},
            type: "post",
            dateType: "json",
            traditional: true,
            success: function (data) {
                alert("加入收藏成功");
                window.location.reload();
            },
            error: function (data) {
                alert("出现错误！！！")
            }
        })
    }
    else {
        alert("没有被选中")
    }
});
// 多选加入简报
$("#in_tags").click(function () {
    var check_obj = document.getElementsByName("onclick_checkbox");
    var check_val = [];
    for (k in check_obj) {
        if (check_obj[k].checked)
            check_val.push(check_obj[k].value);
    }
    console.log(check_val);
    if ($("input[type='checkbox']").is(':checked')) {
        $.ajax({
            url: '/index/spider_add_tags_all/',
            data: {'check_val': check_val,'csrfmiddlewaretoken':$("[name='csrfmiddlewaretoken']").val()},
            type: "post",
            dateType: "json",
            traditional: true,
            success: function (data) {
                alert("加入简报素材成功");
                window.location.reload();
            },
            error: function (data) {
                alert("出现错误！！！")
            }
        })
    }
    else {
        alert("没有被选中")
    }
});
// 批量标为已读
$("#in_eye").click(function () {
    var check_obj = document.getElementsByName("onclick_checkbox");
    var check_val = [];
    for (k in check_obj) {
        if (check_obj[k].checked)
            check_val.push(check_obj[k].value);
    }
    console.log(check_val);
    if ($("input[type='checkbox']").is(':checked')) {
        $.ajax({
            url: '/index/spider_change_see/',
            data: {'check_val': check_val,'csrfmiddlewaretoken':$("[name='csrfmiddlewaretoken']").val()},
            type: "post",
            dateType: "json",
            traditional: true,
            success: function (data) {
                window.location.reload();
            },
            error: function (data) {
                alert("出现错误！！！")
            }
        })
    }
    else {
        alert("没有被选中")
    }
});