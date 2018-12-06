$("#checkbox_on").click(function () {
    // 判断是否已全部选中
    if ($("input[id='checkbox_on']").is(':checked')) {
        // 如果没有全部选中或已全选，点击则取消已选择的checkbox
        $("input[name='onclick_checkbox']:checkbox").each(function () {
            $(this).prop("checked", true);
        })
    } else {
        // 如果都没有选中的话，点击则全部选上
        $("input[name='onclick_checkbox']:checkbox").each(function () {
            $(this).prop("checked", false);
        })
    }
});

$("#many_del").click(function () {
    var check_obj = document.getElementsByName("onclick_checkbox");
    var check_val = [];
    // 获取URL的文件路径
    var url = window.location.pathname;
    console.log(url);
    for (k in check_obj) {
        if (check_obj[k].checked)
            check_val.push(check_obj[k].value);
    }
    if ($("input[type='checkbox']").is(':checked')) {
        $.ajax({
            url: '/del_all/',
            data: {'check_val': check_val, 'url': url, 'csrfmiddlewaretoken':$("[name='csrfmiddlewaretoken']").val()},
            type: "post",
            dateType: "json",
            traditional: true,
            success: function (data) {
                if (url === '/fhsms/'){
                    location.href = "/fhsms/";
                    alert("删除成功")
                }
                if (url === '/pictures/'){
                    location.href = "/pictures/";
                    alert("删除成功")
                }
            }
        })
    }
    else {
        alert("没有被选中")
    }
});