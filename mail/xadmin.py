from xadmin.service.xadmin import x_admin_site as site
from xadmin.service.xadmin import ModelXAdmin
from . import models


site.register(models.Pictures)
site.register(models.StatusMail)
site.register(models.Fhsms)
