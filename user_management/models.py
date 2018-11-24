from django.db import models
from django.contrib.auth.models import User
# 用户模型.
# 第一种：采用的继承方式扩展用户信息（本系统采用）
# 扩展：关联的方式去扩展用户信息
class UserInfo(models.Model):
    user_address = models.CharField(max_length=32, null=True, verbose_name="地址")
    user_phone = models.CharField(max_length=16, unique=True, verbose_name="电话")
    user_stay_years = models.IntegerField(null=True, verbose_name="年限")
    user_status = models.BooleanField(default=True, verbose_name="状态")
    user_gender = models.CharField(max_length=4, verbose_name="性别")
    user_age = models.IntegerField(null=True, verbose_name="年龄")
    user_number = models.CharField(max_length=20, unique=True, verbose_name="编号")
    user_remarks = models.CharField(max_length=255, null=True, verbose_name="备注")
    user_recent_ip = models.CharField(max_length=16, verbose_name="最近的ip")
    user_id_card = models.CharField(max_length=20, unique=True, verbose_name="身份证号")
    user_image = models.ImageField(upload_to="image", default="image/default.jpg", verbose_name="头像")
    user = models.OneToOneField(to=User)



