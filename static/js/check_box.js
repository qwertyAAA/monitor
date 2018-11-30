/*
* 这是一个全选、反选的插件
* 通过全选checkbox(id="check_all")
* 以及子checkbox(class="check_item")
* 来实现
* 并且实现了当子checkbox哪怕有一个未选中时，全选checkbox也不会选中
* */


$(function () {
    $("body").delegate("#check_all", "click",function () {
        if ($(this).prop("checked")) {
            $(".check_item").prop("checked", true)
        }
        else {
            $(".check_item").prop("checked", false)
        }
    });
    $("body").delegate(".check_item", "click", function () {
        var check_flag = true;
        $(".check_item").each(function () {
            if (!$(this).prop("checked")) {
                check_flag = false;
                return false;
            }
        });
        $("#check_all").prop("checked", check_flag)
    });
});