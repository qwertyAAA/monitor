from xadmin.service.xadmin import x_admin_site as site
from . import models

site.register(models.TestTable)
