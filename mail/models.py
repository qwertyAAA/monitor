from django.db import models
from user_management.models import UserInfo

# Create your models here.
class Pictures(models.Model):
    title = models.CharField(max_length=32, verbose_name="标签", default="图片")
    name = models.FileField(upload_to="avatars/", default="default.jpg")
    path = models.FileField(upload_to="avatars/", default="avatars/default.jpg", verbose_name="图片地址")
    BZ = models.CharField(max_length=50, verbose_name="备注")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    master_id = models.ForeignKey(to=UserInfo)


class Fhsms(models.Model):
    content = models.CharField(max_length=9999, verbose_name="邮件内容")
    to_user = models.CharField(max_length=32, verbose_name="发送人")
    from_user = models.ForeignKey(to=UserInfo, verbose_name="接收人")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="发送时间")
    status = models.CharField(max_length=32, verbose_name="邮件状态", choices=((0, '未读'),(1, '已读')))


