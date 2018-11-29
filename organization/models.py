from django.db import models
from user_management import models as m2


# Create your models here.
class Department(models.Model):
    name = models.CharField(max_length=20, null=False)
    en_name = models.CharField(max_length=30, null=False)
    code = models.CharField(max_length=10, null=False)
    phone = models.CharField(max_length=13, null=True)
    address = models.CharField(max_length=20, null=True)
    func = models.CharField(max_length=10, null=True)
    tips = models.TextField(max_length=200, null=True)
    user = models.ForeignKey(to=m2.User)
    top_department = models.ForeignKey(to='self', null=True)
    create_by = models.IntegerField(null=False)

