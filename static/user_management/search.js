
function parXuCommon(i, obj) {
    var collection = $(".conent_ype .spans");
    $.each(collection, function () {
        $(this).removeClass('click');
    });
    $(obj).addClass('click');
}


function attrbuteACommon(i, obj) {
    var collection = $(".switch_type .spans");
    $.each(collection, function () {
        $(this).removeClass('click');
    });
    $(obj).addClass('click');
}


function changeList(i, obj) {
    var collection = $(".source_type .spans");
    $.each(collection, function () {
        $(this).removeClass('click');
    });
    $(obj).addClass('click');
}

function changeLista(i, obj) {
    var collection = $(".title_type .spans");
    $.each(collection, function () {
        $(this).removeClass('click');
    });
    $(obj).addClass('click');
}

function changeListpro(i, obj) {
    var collection = $(".pro .spans");
    $.each(collection, function () {
        $(this).removeClass('click');
    });
    $(obj).addClass('click');
}

function Sourcewebsite(i, obj) {
    var collection = $(".Source_website .spans");
    $.each(collection, function () {
        $(this).removeClass('click');
    });
    $(obj).addClass('click');
}


function informationtype(i, obj) {
    var collection = $(".information_type .spans");
    $.each(collection, function () {
        $(this).removeClass('click');
    });
    $(obj).addClass('click');
}

function displaytype(i, obj) {
    var collection = $(".display_type .spans");
    $.each(collection, function () {
        $(this).removeClass('click');
    });
    $(obj).addClass('click');
}
function warningtype(i, obj) {
    var collection = $(".warning_type .spans");
    $.each(collection, function () {
        $(this).removeClass('click');
    });
    $(obj).addClass('click');
}

var ds = $("span").document.getElementById('.click');