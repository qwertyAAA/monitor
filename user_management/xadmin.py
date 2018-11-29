from xadmin.service.xadmin import x_admin_site as site
from xadmin.service.xadmin import ModelXAdmin
from user_management.models import UserInfo, User
from xadmin.service.xadmin import ModelXAdmin

site.register(UserInfo)
site.register(User)
