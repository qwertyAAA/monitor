from django import template
from menu_management import models
from permission import models as per_models

register = template.Library()


@register.inclusion_tag('tags_html/menu.html')
def get_menu(request):
    #当用户登录的时候
    if not request.user.is_anonymous:
        per_first_list=request.session.get('first_menu_list')
        per_second_list=request.session.get('second_menu_list')
        print(per_second_list)
        per_first_menu = per_models.Permission.objects.filter(id__in=per_first_list)
        per_second_menu = per_models.Permission.objects.filter(id__in=per_second_list)
        per_first_title=[]
        per_second_title=[]
        print(per_second_menu,per_first_menu)
        #向菜单表里面插入数据,已经存在的不再插入
        for first in per_first_menu:
            flag1=models.First_Menu.objects.filter(action=first.title).first()
            if not flag1:
                new_menu=models.First_Menu.objects.create(title=first.title,action=first.title)
                for second in per_second_menu:
                    flag2=models.Second_Menu.objects.filter(action=second.url)
                    if (not flag2) and (second.group_id == first.id):
                        models.Second_Menu.objects.create(title=second.title,url=second.url,action=second.url,first_menu_id=new_menu.nid)
        #获取所有有权限的菜单的action
        for first in per_first_menu:
                per_first_title.append(first.title)
                for second in per_second_menu:
                    per_second_title.append(second.url)
    #查询有权限的菜单
        first_menu=models.First_Menu.objects.filter(status=True,action__in=per_first_title)
        second_menu=models.Second_Menu.objects.filter(status=True,action__in=per_second_title)
        print(per_first_title,per_second_title)
        return {'first_menu': first_menu,'second_menu':second_menu}
    #当用户没有登录的时候
    else:
        return {'first_menu': [], 'second_menu': []}
