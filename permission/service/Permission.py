from permission.models import Role
from permission.models import Permission
from permission.models import RoleGroup
from django.db.models import Q
def init_permission(user_obj, request):
    print(user_obj.is_superuser)
    if user_obj.is_superuser:
        #如果是超级用户登录，获得角色表中的第一个角色，并为其赋予所有权限，并将  该超级用户与该角色对应
        role_obj=Role.objects.all().first()
        permisson_list=Permission.objects.all()
        role_obj.permissions.clear()
        role_obj.permissions.add(*permisson_list)
        user_obj.role_set.clear()
        user_obj.role_set.add(role_obj)
    else:
        #如果是普通用户登录
        print(1)
        print(user_obj.role_set.all().count())
        print(user_obj.role_set.all().exists())
        print(type(user_obj.role_set.all()))

        if user_obj.role_set.all().exists():
            #如果该用户有对应的角色
            print(2)
            pass

        else:                   #注册后第一次登录，没有对应的角色
            print(3)
            role_obj2=Role.objects.filter(title='游客').first()
            permission_list2=Permission.objects.filter(Q(action='list') | Q(action='list_second'))
            role_obj2.permissions.clear()
            role_obj2.permissions.add(*permission_list2)
            user_obj.role_set.add(role_obj2)

    # 方案1
    # request.session['user_id'] = user_obj.pk
    # # 查询当前用户的所有的权限  放在session中
    # # result=user_obj.roles.all() #queryset  所有角色
    # # 得到所有的角色所对应的权限url
    # permissons = user_obj.roles.all().values("permissions__url").distinct()
    # # ['/users/add/','/users/']
    # permissons_list = []
    # for item in permissons:
    #     permissons_list.append(item['permissions__url'])
    # print(permissons_list)
    # request.session['permission_list'] = permissons_list

    # 方案2 user  url[]  action[]  groupid
    # {1:{urls:[],actions:[]}}

    #获取该user对象的所有角色的所有权限
    permisson = user_obj.role_set.all().values("permissions__url", "permissions__action",'permissions__group_id').distinct()
    # print(user_obj.role_set.all())
    # print("该用户的权限信息如下：")
    # print(permisson)
    # print("**"*10)

    permisson_dict = {}

    data_permission = user_obj.role_set.all().values('data_per__id').distinct()
    # print('数据权限id', data_permission)
    data_permission_id_list=[]
    for i in data_permission:
        data_permission_id_list.append(i['data_per__id'])
    request.session['data_permission_id_list']=data_permission_id_list

    for item in permisson:
        gid = item.get('permissions__group_id')

        if not gid in permisson_dict:

            permisson_dict[gid] = {
                "urls": [item.get('permissions__url'), ],
                'actions': [item.get("permissions__action"), ]
            }
        else:
            permisson_dict[gid]['urls'].append(item.get('permissions__url'))
            permisson_dict[gid]['actions'].append(item.get('permissions__action'))

    #根据权限组id  得到该角色的权限分组 {1:{urls:[],actions:[]}}
    # print(permisson_dict)
    # print("**" * 10)

    #放入session中
    request.session['permisson_dict'] = permisson_dict

    # 左侧菜单
    #获取该用户的所有权限信息
    permission_menu = user_obj.role_set.all().values('permissions__url', 'permissions__action',
                                                  'permissions__group__title','permissions__id').distinct()

    menu_permission_list = []
    first_menu_list=[]
    second_menu_list=[]

    for item in permission_menu:
        if item['permissions__action'] == 'list':
            menu_permission_list.append((item['permissions__url'], item['permissions__group__title']))
            first_menu_list.append(item['permissions__id'])
        if item['permissions__action'] == 'list_second':
            second_menu_list.append(item['permissions__id'])


    # print(menu_permission_list)
    # print(first_menu_list)
    # print(second_menu_list)
    request.session['menu_permission_list'] = menu_permission_list
    request.session['first_menu_list'] = first_menu_list
    request.session['second_menu_list'] = second_menu_list
