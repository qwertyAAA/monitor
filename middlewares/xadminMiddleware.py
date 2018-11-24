from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse, render, redirect


class CheckXadminAuth(MiddlewareMixin):
    @staticmethod
    def process_request(request):
        split_urls = request.path_info.split("/")
        if split_urls[1] == "xadmin":
            if request.user.is_superuser:
                return
            error_msg = "您没有管理权限！"
            return render(request, "xadmin/xadmin_login.html", {"error_msg": error_msg})
        return


class CheckXadminLogin(MiddlewareMixin):
    @staticmethod
    def process_request(request):
        split_urls = request.path_info.split("/")
        if split_urls[1]:
            if request.user.is_anonymous:
                error_msg = "请您先登陆！"
                return render(request, "xadmin/xadmin_login.html", {"error_msg": error_msg})
            return
        return
