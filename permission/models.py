from django.db import models
from django.contrib.auth.models import User
from user_management.models import UserInfo
# Create your models here.

class Role(models.Model):
    title=models.CharField(max_length=32,verbose_name='角色名称')
    permissions=models.ManyToManyField(to='Permission')
    group=models.ForeignKey(to='RoleGroup')
    user=models.ManyToManyField(to=User)
    def __str__(self): return self.title

class RoleGroup(models.Model):
    title=models.CharField(max_length=32,verbose_name='角色组名称')
    permissions = models.ManyToManyField(to='Permission')

class Permission(models.Model):
    title=models.CharField(max_length=32,verbose_name="权限名字")
    url=models.CharField(max_length=32,verbose_name='权限URL')  #user/add  add  users list users/delete/1  delete
    action=models.CharField(max_length=32,verbose_name="权限Action")
    group=models.ForeignKey(to="PermissionGroup")
    is_del=models.BooleanField(default=False)

    def __str__(self): return self.title


class PermissionGroup(models.Model):
    title=models.CharField(max_length=32,verbose_name="权限组名称")
    is_del=models.BooleanField(default=False)

    def __str__(self): return self.title
