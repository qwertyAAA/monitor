from django.utils.deprecation import  MiddlewareMixin
from django.shortcuts import HttpResponse,redirect,render
import  re

class ValidPermission(MiddlewareMixin):

    def process_request(self, request):

        #检验白名单的
        current_path = request.path_info  # 当前路径
        print(current_path)

        valid_url_list=['/login/','/register/','/admin/.*']

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

        #方案2

        permission_dict=request.session.get('permisson_dict')

        for item in permission_dict.values():  #{urs  actions}
            urls=item['urls']
            for permisson in urls:
                permisson="^%s$"%permisson
                result=re.match(permisson,current_path)
                if result:
                    request.actions=item['actions']
                    return None

        return HttpResponse('没有操作权限')














