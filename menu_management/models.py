from django.db import models

# Create your models here.
class First_Menu(models.Model):
    nid=models.AutoField(primary_key=True,verbose_name='编号')
    title=models.CharField(max_length=30,null=False,verbose_name='顶级菜单',unique=True)
    ico=models.CharField(max_length=40,default='menu-icon fa fa-caret-right',verbose_name='图标')
    status=models.BooleanField(default=True,verbose_name='状态')
    remark=models.CharField(max_length=100,null=True,verbose_name='备注')

    def __str__(self):
        return self.title

class Second_Menu(models.Model):
    nid=models.AutoField(primary_key=True,verbose_name='编号')
    title=models.CharField(max_length=30,null=False,verbose_name='二级菜单')
    url=models.CharField(max_length=40,default=None,verbose_name='链接')
    ico = models.CharField(max_length=40, default='menu-icon fa fa-caret-right', verbose_name='图标')
    status = models.BooleanField(default=True, verbose_name='状态')
    remark=models.CharField(max_length=100,null=True,verbose_name='备注')
    first_menu = models.ForeignKey(to=First_Menu)

    def __str__(self):
        return self.title