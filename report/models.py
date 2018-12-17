from django.db import models


# Create your models here.

class Mould(models.Model):
    name = models.CharField(max_length=20)
    url = models.TextField(max_length=100)
    key = models.CharField(max_length=100)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Report(models.Model):
    name = models.CharField(max_length=30, default='舆情简报')
    create_time = models.DateField(auto_now_add=True)
    tieba_num = models.IntegerField()
    blog_num = models.IntegerField()
    sensitive = models.IntegerField()
    no_sensitive = models.IntegerField()
    mould = models.ForeignKey(to=Mould)

    def __str__(self):
        return self.name
