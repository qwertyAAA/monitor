$("#fuzzy-query").click(function () {
    var search = $("#search_id").val();     // 获取查询框内容
    var action_time = $("#action-time").val();    // 获取查询开始时间
    var end_time = $("#end-time").val();    // 获取查询结束时间
    var select_id = $("#select_text").val();    // 获取读状态
    var csrfToken = $("[name='csrfmiddlewaretoken']").val();
    $(".table tbody").html("");
    $.ajax({
        url: "/fuzzy_query/",
        type: "post",
        data: {
            "search": search,
            "action_time": action_time,
            "end_time": end_time,
            "select_id": select_id,
            "csrfmiddlewaretoken": csrfToken,
        },
        success: function (data) {
            if (data.status) {
                $(".table tbody").append(data.html)
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
$("#fuzzy-query1").click(function () {
    var search = $("#search_id").val();     // 获取查询框内容
    var action_time = $("#action-time").val();    // 获取查询开始时间
    var end_time = $("#end-time").val();    // 获取查询结束时间
    var csrfToken = $("[name='csrfmiddlewaretoken']").val();
    $(".table tbody").html("");
    $.ajax({
        url: "/fuzzy_query1/",
        type: "post",
        data: {
            "search": search,
            "action_time": action_time,
            "end_time": end_time,
            "csrfmiddlewaretoken": csrfToken,
        },
        success: function (data) {
            if (data.status) {
                $(".table tbody").append(data.html)
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