from django.utils.deprecation import  MiddlewareMixin
from django.shortcuts import HttpResponse,redirect,render
import re

class ValidPermission(MiddlewareMixin):

    def process_request(self, request):

        #检验白名单的
        current_path = request.path_info  # 当前路径
        print(current_path)

        valid_url_list=['/login/','/register/','/admin/.*','/xadmin/','/logout/',
                        '/register/','/base/','/fhsms/','/pictures/','/media/.*',
                        '/index/',]

        for valid_url in valid_url_list:
            result=re.match(valid_url,current_path)
            if result:
                return

        #检验用户登录的
        user_id=request.session.get('user_id')
        if not user_id:
            return redirect('/login/')


        '''
        判断用户权限过滤的
        :param request:
        :return: None  正常执行url 否则显示没有访问权限
        '''

        #方案1

        # permission_list = request.session.get('permission_list', [])  # ['users/delete/(\d+)']
        #
        # for permission in permission_list:
        #     permission='^%s$'%permission
        #     result = re.match(permission, current_path)
        #     if result:
        #         return None
        # #
        # # if current_path in permission_list:
        # #     flag=True
        # return HttpResponse('没有访问权限')

        #判断数据权限
        data_permission_id_list = request.session.get('data_permission_id_list')
        print(data_permission_id_list)
        if 3 in data_permission_id_list:    #可以查看所有的数据
            pass
        elif 2 in data_permission_id_list:  #可以看本部门的数据
            pass
        elif 1 in data_permission_id_list:  #仅可见自己的数据
            pass



        #方案2

        permission_dict=request.session.get('permisson_dict')
        print(permission_dict)
        for item in permission_dict.values():  #{urs  actions}
            urls=item['urls']
            print('***')
            print(urls)
            print('***')
            for permisson in urls:
                permisson="^%s$"%permisson
                print(permisson)
                result=re.match(permisson,current_path)
                print(result)
                if result:
                    request.actions=item['actions']
                    return None
        return HttpResponse('没有操作权限')














