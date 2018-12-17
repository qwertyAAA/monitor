from xadmin.service.xadmin import x_admin_site as site
from xadmin.service.xadmin import ModelXAdmin
from . import models


site.register(models.Article)
site.register(models.Author)
site.register(models.Source)
site.register(models.Classify)
site.register(models.Rule)
