from xadmin.service.xadmin import x_admin_site as site
from xadmin.service.xadmin import ModelXAdmin
from . import models


class TestTable1XAdmin(ModelXAdmin):
    field_names = ["name", "password", "address"]


site.register(models.TestTable)
site.register(models.TestTable1)
