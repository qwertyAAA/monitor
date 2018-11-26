from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse, render, redirect


class CheckXadminPermission(MiddlewareMixin):
    @staticmethod
    def process_request(request):
        split_urls = request.path_info.split("/")
        if split_urls[1] == "xadmin":
            superuser = request.user.is_superuser
            anonymous = request.user.is_anonymous
            if not superuser or anonymous:
                error_msg = ""
                if not superuser:
                    error_msg = "sorry, 您没有管理权限！"
                if anonymous:
                    error_msg = "请您先登陆！"
                return render(request, "xadmin/xadmin_permission.html", {"error_msg": error_msg})
            return
        return

