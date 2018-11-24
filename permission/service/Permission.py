def init_permission(user_obj, request):
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
    permissons = user_obj.roles.all().values("permissions__url", "permissions__action",
                                             'permissions__group_id').distinct()

    # print(permissons)

    permissons_dict = {}

    for item in permissons:
        gid = item.get('permissions__group_id')

        if not gid in permissons_dict:

            permissons_dict[gid] = {
                "urls": [item.get('permissions__url'), ],
                'actions': [item.get("permissions__action"), ]

            }
        else:
            permissons_dict[gid]['urls'].append(item.get('permissions__url'))
            permissons_dict[gid]['actions'].append(item.get('permissions__action'))

    # print(permissons_dict)

    request.session['permisson_dict'] = permissons_dict

    # 左侧菜单

    permission_menu = user_obj.roles.all().values('permissions__url', 'permissions__action',
                                                  'permissions__group__title').distinct()

    print(permission_menu)

    menu_permission_list = []

    for item in permission_menu:
        if item['permissions__action'] == 'list':
            menu_permission_list.append((item['permissions__url'], item['permissions__group__title']))

    print(menu_permission_list)

    request.session['menu_permission_list'] = menu_permission_list
