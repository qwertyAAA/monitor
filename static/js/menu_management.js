// 添加一级菜单时判断是否已经存在
$('body').delegate('#first_menu_name', 'blur', function () {
    var menu_name=$(this).val();
    $.ajax({
        url:'/menu/add/first/',
        type:'get',
        data:{
            'menu_name':menu_name
        },
        success:function (data) {
            console.log('一级菜单');
            if (data.span == '1') {
                $('#prompt').css('display','block');
                $('#sub_btn').attr('disabled','disabled')
            }
            else
            {
                $('#prompt').css('display','none');
                $('#sub_btn').removeAttr('disabled')
            }
            if ($('#first_menu_name').val().length == 0)
            {
                $('#sub_btn').attr('disabled','disabled')
            }
        }
    });
});
if ($('#first_menu_name').val().length == 0)
{
    $('#sub_btn').attr('disabled','disabled')
}

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
            var edit_btnid='#edit_btn'+data.id;
            if (data.span == '1') {
                $(edit_id).css('display','block');
                $(edit_btnid).attr('disabled','disabled')
            }
            else
            {
                $(edit_id).css('display','none');
                $(edit_btnid).removeAttr('disabled')
            }
            if(menu_name.length == 0){
                $(edit_btnid).attr('disabled','disabled')
            }
        }
    });
});
