class OnlineUser(object):
    def __init__(self):
        self.users = []


online_users = OnlineUser()


def offline(request):
    if request.user in online_users.users:
        online_users.users.remove(request.user)
    print(online_users.users, "1111111111111111111111111")


def online(request):
    if (not request.user.is_anonymous()) and (request.user not in online_users.users):
        online_users.users.append(request.user)
    print(online_users.users, "2222222222222222222")