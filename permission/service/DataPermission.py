from django.contrib.auth.models import User
from django.db.models import  Q
from user_management.models import UserInfo
def has_data(request):

    # 判断数据权限
    data_permission_id_list = request.session.get('data_permission_id_list')
    # print(data_permission_id_list)
    if 3 in data_permission_id_list:  # 可以查看所有的数据
        return 3
    elif 2 in data_permission_id_list:  # 可以看本部门的数据
        return 2
    elif 1 in data_permission_id_list:  # 仅可见自己的数据
        return 1
