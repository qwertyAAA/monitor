from django import template
from menu_management import models
from permission import models as per_models
register=template.Library()

@register.inclusion_tag('tags_html/menu.html')
def get_menu():
    # first_menu=[]
    # second_menu=[]
    first_menu=models.First_Menu.objects.all()
    print(len(first_menu))
    if len(first_menu) == 0:
        per_group=per_models.PermissionGroup.objects.all()
        print(per_group)
        for i in per_group:
            #id=999对应的是增删改查的权限组不应该在菜单里面出现
            if i.id!=999 and i.is_del==False:
                menu=models.First_Menu.objects.create(title=i.title)
                # first_menu.append(i)
                for j in i.permission_set.all():
                    models.Second_Menu.objects.create(title=j.title,first_menu_id=menu.nid,url=j.url)
    first_menu=models.First_Menu.objects.all()
    return {'first_menu':first_menu}
