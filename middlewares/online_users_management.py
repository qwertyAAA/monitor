from django.utils.deprecation import MiddlewareMixin


class OnlineUser(object):
    def __init__(self):
        self.users = []


online_users_management = OnlineUser()


class OnlineManagement(MiddlewareMixin):
    @staticmethod
    def process_request(request):
        if not request.user.is_anonymous:
            online_status = request.GET.get("online_status")
            if request.user not in online_users_management.users:
                if online_status == "online":
                    online_users_management.users.append(request.user)
            else:
                if online_status == "offline" or request.path_info == "/logout/":
                    online_users_management.users.remove(request.user)
        return


def get_online_users_count(request):
    print(online_users_management.users)
    return {"online_users_count": len(online_users_management.users)}
