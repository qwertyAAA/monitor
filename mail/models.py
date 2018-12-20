from django.db import models
from user_management.models import UserInfo
from django.contrib.auth.models import User


# Create your models here.
class Pictures(models.Model):
    """
    图片表
    """
    title = models.CharField(max_length=32, verbose_name="标签", default="图片")
    name = models.CharField(max_length=32, default="图片")
    path = models.FileField(upload_to="avatars/", default="avatars/default.jpg", verbose_name="图片地址")
    BZ = models.CharField(max_length=50, verbose_name="备注", default="图片管理处上传")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    master_id = models.ForeignKey(to=User, verbose_name="图片主人")

    def __str__(self):
        return self.title


class StatusMail(models.Model):
    """
    邮件状态表
    """
    nid = models.IntegerField(primary_key=True)
    status = models.CharField(max_length=32, verbose_name="邮件状态")

    def __str__(self):
        return self.status


class Fhsms(models.Model):
    """
    邮件or站内信表
    """
    title = models.CharField(max_length=32, verbose_name="标签")
    content = models.CharField(max_length=9999, verbose_name="邮件内容")
    to_user = models.CharField(max_length=32, verbose_name="发送人")
    from_user = models.ForeignKey(to=User, verbose_name="接收人")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="发送时间")
    status_id = models.ForeignKey(to=StatusMail)

    def __str__(self):
        return self.title
