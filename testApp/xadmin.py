from xadmin.service.xadmin import x_admin_site as site
from testApp.models import TestTable

# Register your models here.
site.register(TestTable)
