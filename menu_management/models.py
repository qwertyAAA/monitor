from django.db import models

# Create your models here.
class Menu(models.Model):
    title_list=models.CharField(max_length=9999,null=False,verbose_name='菜单列表')

    def __str__(self):
        return self.title_list