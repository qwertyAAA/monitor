from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import render, redirect, HttpResponse
from mail.models import Fhsms


class AllRequest(object):
    def __init__(self):
        self.requests_list = []
        self.requests_user_pk = []


all_requests = AllRequest()


class PushRequests(MiddlewareMixin):
    @staticmethod
    def process_request(request):
        if not request.user.is_anonymous:
            if request.user.pk not in all_requests.requests_user_pk:
                all_requests.requests_list.append(request)
                all_requests.requests_user_pk.append(request.user.pk)


def get_online_requests_count(request):
    return {"online_requests_count": len(all_requests.requests_list)}


def base(request):
    user_id = request.user.id
    status_id = Fhsms.objects.filter(from_user_id=user_id).values('status_id_id')
    print(status_id)
    sum_email = 0
    for i in status_id:
        if i['status_id_id'] == 0:
            sum_email += 1
    return {'sum_email': sum_email}
