// 添加一级菜单时判断是否已经存在
$('body').delegate('#first_menu_name', 'blur', function () {
    console.log('nihao');
    var menu_name=$(this).val();
    $.ajax({
        url:'/menu/add/first/',
        type:'get',
        data:{
            'menu_name':menu_name
        },
        success:function (data) {
            if (data.span == '1') {
                $('#prompt').css('display','block');
                $('#sub_btn').attr('disabled','disabled')
            }
            else
            {
                $('#prompt').css('display','none');
                $('#sub_btn').removeAttr('disabled')
            }
        }
    });
});

// 添加二级菜单时判断是否已经存在
$('body').delegate('#second_menu_name', 'blur', function () {
    var menu_name = $(this).val();
    console.log($('#second_prompt').css('display'));
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
                if ($('#second_path_prompt').css('display') == 'none' && $('#second_prompt').css('display') == 'none')
                {
                    $('#second_btn').removeAttr('disabled')
                }
                // $('#second_btn').removeAttr('disabled')
            }
        }
    });
});
$('body').delegate('#menu_path', 'blur', function () {
    var menu_path=$(this).val();
    $.ajax({
        url:'/menu/add/second/',
        type:'get',
        data:{
            'menu_path':menu_path
        },
        success:function (data) {
            if (data.span == '2') {
                $('#second_path_prompt').css('display','block');
                $('#second_btn').attr('disabled','disabled')
            }
            if (data.span == '3')
            {
                $('#second_path_prompt').css('display','none');
                // 只有path和title全部通过校验提交按钮才可以点击
                if ($('#second_path_prompt').css('display') == 'none' && $('#second_prompt').css('display') == 'none')
                {
                    $('#second_btn').removeAttr('disabled')
                }
                // $('#second_btn').removeAttr('disabled')
            }
        }
    });
  });



// 编辑一级菜单时进行数据校验
$('body').delegate('.edit_menuname', 'blur', function () {
    var menu_name=$(this).val();
    var menu_id=$(this).attr('menuid');
    $.ajax({
        url:'/menu/edit/first/0/',
        type:'get',
        data:{
            'menu_name':menu_name,
            'menu_id':menu_id
        },
        success:function (data) {
            console.log(data.id);
            var edit_id='#edit_prompt'+data.id;
            if (data.span == '1') {
                $(edit_id).css('display','block');
                $('#edit_btn').attr('disabled','disabled')
            }
            else
            {
                $(edit_id).css('display','none');
                $('#edit_btn').removeAttr('disabled')
            }
        }
    });
});

// 编辑二级菜单时进行数据校验
$('body').delegate('.edit_second_menuname', 'blur', function () {
    var menu_name=$(this).val();
    var menu_id=$(this).attr('menuid');
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
                if ($(edit_id).css('display') == 'none' && $(edit_path_id).css('display') == 'none')
                {
                    $(submit_btn).removeAttr('disabled')
                }
            }
        }
    });
});
$('body').delegate('.edit_second_menupath', 'blur', function () {
    var menu_path=$(this).val();
    var menu_id=$(this).attr('menuid');
    $.ajax({
        url:'/menu/edit/second/0/',
        type:'get',
        data:{
            'menu_path':menu_path,
            'menu_id':menu_id
        },
        success:function (data) {
            console.log(data.id);
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
                if ($(edit_id).css('display') == 'none' && $(edit_path_id).css('display') == 'none')
                {
                    $(submit_btn).removeAttr('disabled')
                }
            }
        }
    });
});