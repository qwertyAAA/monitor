from django.db import models
from django.contrib.auth.models import User


# 用户模型.
# 第一种：采用的继承方式扩展用户信息（本系统采用）
# 扩展：关联的方式去扩展用户信息
class UserInfo(models.Model):
    user_address = models.CharField(max_length=32, null=True, verbose_name="地址")
    user_phone = models.CharField(max_length=16, unique=True, verbose_name="电话")
    # user_department=models
    user_stay_years = models.IntegerField(null=True, verbose_name="年限")
    user_status = models.BooleanField(default=True, verbose_name="状态")
    user_gender = models.CharField(max_length=4, verbose_name="性别")
    user_name = models.CharField(max_length=32, default='name', verbose_name="姓名", null=True)
    user_age = models.IntegerField(null=True, verbose_name="年龄")
    user_number = models.CharField(max_length=20, unique=True, verbose_name="编号")
    user_remarks = models.CharField(max_length=255, null=True, verbose_name="备注")
    user_recent_ip = models.CharField(max_length=16, verbose_name="最近的ip")
    user_id_card = models.CharField(max_length=20, unique=True, verbose_name="身份证号")
    user_image = models.ImageField(upload_to="avatars/", default="avatars/default.jpg", verbose_name="头像")
    user = models.OneToOneField(to=User)


# 通讯录表
class Mail_list(models.Model):
    mail_phone = models.CharField(max_length=16, unique=True, verbose_name="电话")
    mail_name = models.CharField(max_length=32, default='name', verbose_name="姓名", null=True)
    mail_remarks = models.CharField(max_length=255, null=True, verbose_name="备注")
    mail_email = models.CharField(max_length=255, null=True, verbose_name="邮箱")
    mail_weixin_number = models.CharField(max_length=16, unique=True, verbose_name="微信号")
    mail_company = models.CharField(max_length=32, default='name', verbose_name="单位", null=True)



class System_setup(models.Model):
    Scheme_name = models.CharField(max_length=16,  verbose_name="方案名称")
    warning_content = models.CharField(max_length=32, default='name', verbose_name="预警内容", null=True)
    warning_type = models.CharField(max_length=255, null=True, verbose_name="预警类型")
    warning_mode = models.CharField(max_length=255, null=True, verbose_name="预警方式")
    switch = models.CharField(max_length=16, unique=True, verbose_name="开关")

