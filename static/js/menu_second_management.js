// 添加二级菜单的时候对数据进行校验
$('body').delegate('#second_menu_name', 'blur', function () {
    var menu_name = $(this).val();
    $.ajax({
        url: '/menu/add/second/',
        type: 'get',
        data: {
            'menu_name': menu_name
        },
        success: function (data) {
            if (data.span == '1') {
                $('#second_prompt').css('display', 'block');
                $('#second_btn').attr('disabled', 'disabled')
            }
            else {
                $('#second_prompt').css('display', 'none');
                // 只有path和title全部通过校验提交按钮才可以点击
                if ($('#second_path_prompt').css('display') == 'none' && $('#second_prompt').css('display') == 'none') {
                    $('#second_btn').removeAttr('disabled')
                }
            }
            console.log($('#menu_path').val().length);
            if ($('#second_menu_name').val().length == 0 || $('#menu_path').val().length == 0) {
                $('#second_btn').attr('disabled', 'disabled')
            }
        }
    });
});
$('body').delegate('#menu_path', 'blur', function () {
    var menu_path = $(this).val();
    $.ajax({
        url: '/menu/add/second/',
        type: 'get',
        data: {
            'menu_path': menu_path
        },
        success: function (data) {
            if (data.span == '2') {
                $('#second_path_prompt').css('display', 'block');
                $('#second_btn').attr('disabled', 'disabled')
            }
            if (data.span == '3') {
                $('#second_path_prompt').css('display', 'none');
                // 只有path和title全部通过校验提交按钮才可以点击
                if ($('#second_path_prompt').css('display') == 'none' && $('#second_prompt').css('display') == 'none') {
                    $('#second_btn').removeAttr('disabled')
                }
            }
            // 当菜单名或者path有一个为空的时候禁止提交按钮
            if ($('#second_menu_name').val().length == 0 || $('#menu_path').val().length == 0) {
                $('#second_btn').attr('disabled', 'disabled')
            }
        }
    });
});
// 页面加载的时候当菜单名和path为空时候禁止提交按钮
if ($('#second_menu_name').val().length == 0 || $('#menu_path').val().length == 0) {
    $('#second_btn').attr('disabled', 'disabled')
}

// 编辑二级菜单时进行数据校验
$('body').delegate('.edit_second_menuname', 'blur', function () {
    var menu_name=$(this).val();
    var menu_id=$(this).attr('menuid');
    var menu_path=$(this).parent('div').parent('div').next('div').children('div').children('input').val();
    $.ajax({
        url:'/menu/edit/second/0/',
        type:'get',
        data:{
            'menu_name':menu_name,
            'menu_id':menu_id
        },
        success:function (data) {
            var edit_id='#edit_second_prompt'+data.id;
            var edit_path_id='#second_edit_path_prompt'+data.id;
            var submit_btn='#edit_second_sbtn'+data.id;
            if (data.span == '1') {
                $(edit_id).css('display','block');
                $(submit_btn).attr('disabled','disabled')
            }
            else
            {
                $(edit_id).css('display','none');
                // 只有当输入的名字和路径名且都不为空的时候才能让提交按钮启动
                if ($(edit_id).css('display') == 'none' && $(edit_path_id).css('display') == 'none' && menu_name.length > 0 && menu_path.length >0)
                {
                    $(submit_btn).removeAttr('disabled')
                }
            }
            if(menu_name.length == 0 || menu_path.length == 0){
                $(submit_btn).attr('disabled','disabled')
            }
        }
    });
});
$('body').delegate('.edit_second_menupath', 'blur', function () {
    var menu_path=$(this).val();
    var menu_id=$(this).attr('menuid');
    var menu_name = $(this).parent('div').parent('div').prev('div').children('div').children('input').val();
    $.ajax({
        url:'/menu/edit/second/0/',
        type:'get',
        data:{
            'menu_path':menu_path,
            'menu_id':menu_id
        },
        success:function (data) {
            var edit_path_id='#second_edit_path_prompt'+data.id;
            var submit_btn='#edit_second_sbtn'+data.id;
            var edit_id='#edit_second_prompt'+data.id;
            if (data.span == '2') {
                $(edit_path_id).css('display','block');
                $(submit_btn).attr('disabled','disabled')
            }
            if (data.span == '3')
            {
                $(edit_path_id).css('display','none');
                // 只有当输入的名字和路径名且都不为空的时候才能让提交按钮启动
                if ($(edit_id).css('display') == 'none' && $(edit_path_id).css('display') == 'none' && menu_path.length>0 && menu_name.length>0)
                {
                    $(submit_btn).removeAttr('disabled')
                }
            }
            if(menu_path.length == 0 || menu_name.length == 0){
                $(submit_btn).attr('disabled','disabled')
            }
        }
    });
});
