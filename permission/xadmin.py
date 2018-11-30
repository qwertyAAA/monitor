from xadmin.service.xadmin import x_admin_site as site
from xadmin.service.xadmin import ModelXAdmin
from . import models


site.register(models.Permission)
site.register(models.Role)
site.register(models.PermissionGroup)
site.register(models.Data_Per)
site.register(models.RoleGroup)
