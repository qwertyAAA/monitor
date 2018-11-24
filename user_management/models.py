
from django.db import models
from django.contrib.auth.models import User

# 用户信息表
class UserInfo(models.Model):
    # user_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(to=User, to_field="id", verbose_name="用户")
    user_address = models.CharField(max_length=32, null=True, verbose_name="地址")
    user_grade=models.CharField(max_length=32, null=True, verbose_name="等级")
    user_phone = models.CharField(max_length=16, null=True, verbose_name="电话")
    Due_time=models.CharField(max_length=16, null=True, verbose_name="到期时间")
    user_stay_years=models.CharField(max_length=16, null=True, verbose_name="年限")
    user_gender = models.CharField(max_length=4, verbose_name="性别")
    user_age = models.IntegerField(null=True, verbose_name="编号")
    user_number = models.CharField(max_length=16, null=True, verbose_name="电话")
    user_remarks=models.CharField(max_length=32, null=True, verbose_name="备注")
    user_recentip=models.CharField(max_length=16, null=True, verbose_name="最近的ip")
    def __str__(self):
        return self.user.username






