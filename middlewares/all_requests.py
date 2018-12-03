from django.utils.deprecation import MiddlewareMixin


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
