function selectTimeSubmit(time, i, obj) {
    var collection = $(".time_size .spans");
    $.each(collection, function () {
        $(this).removeClass('click');
    });
    $(obj).addClass('click');
}

function parXuCommon(i, obj) {
    var collection = $(".article_ranking .spans");
    $.each(collection, function () {
        $(this).removeClass('click');
    });
    $(obj).addClass('click');
}

function attrbuteACommon(i, obj) {
    var collection = $(".article_ranking .span_right .attribute_right .spans");
    $.each(collection, function () {
        $(this).removeClass('click');
    });
    $(obj).addClass('click');
}

function changeList(i, obj) {
    var collection = $(".results_show .spans");
    $.each(collection, function () {
        $(this).removeClass('click');
    });
    $(obj).addClass('click');
}

function changeCombineFlag(i, obj) {
    var collection = $(".results_show .span_right .merge_right .spans");
    $.each(collection, function () {
        $(this).removeClass('click');
    });
    $(obj).addClass('click');
}

function isSearchRootWb(i, obj) {
    var collection = $(".micro_blog .spans");
    $.each(collection, function () {
        $(this).removeClass('click');
    });
    $(obj).addClass('click');
}

function changeInvolveWay(i, obj) {
    var collection = $(".micro_blog .span_right .involve_right .spans");
    $.each(collection, function () {
        $(this).removeClass('click');
    });
    $(obj).addClass('click');
}

function changeKeywordProvince(i, obj) {
    var collection = $(".region .spans");
    $.each(collection, function () {
        $(this).removeClass('click');
    });
    $(obj).addClass('click');
}

function changeMatchingMode(i, obj) {
    var collection = $(".region .span_right .matching_right .spans");
    $.each(collection, function () {
        $(this).removeClass('click');
    });
    $(obj).addClass('click');
}

function changeWeiboType(i, obj) {
    var collection = $(".blog_content .spans");
    $.each(collection, function () {
        $(this).removeClass('click');
    });
    $(obj).addClass('click');
}

function cptWebSiteCommon(i, obj) {
    var collection = $(".source_website .spans");
    $.each(collection, function () {
        $(this).removeClass('click');
    });
    $(obj).addClass('click');
}

// $(".content_50").read(function () {
//
//     var content = document.getElementById(".content_50").firstChild.nodeValue;
//     console.log(content);
// });
// $(function () {
//     //加载事件
//     var collection = $(".spans");
//     $.each(collection, function () {
//         $(this).addClass("start");
//     });
// });
//
// //单击事件
// function selectTimeSubmit(dom) {
//     var collection = $(".spans");
//     $.each(collection, function () {
//         $(this).removeClass("end");
//         $(this).addClass("start");
//     });
//     $(dom).removeClass("start");
//     $(dom).addClass("end");
// }
