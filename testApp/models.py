from django.db import models


# Create your models here.
class TestTable(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class TestTable1(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32, verbose_name="名字")
    password = models.CharField(max_length=32, verbose_name="密码")
    address = models.CharField(max_length=32, verbose_name="地址")