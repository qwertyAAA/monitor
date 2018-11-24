from django.db import models

# Create your models here.
class Company(models.Model):
    name = models.CharField(max_length=20, null=False)
    english_name = models.CharField(max_length=30, null=False)

class Department(models.Model):
    name = models.CharField(max_length=20, null=False)
    english_name = models.CharField(max_length=30, null=False)
    company = models.ForeignKey(to=Company)
