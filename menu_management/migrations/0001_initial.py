# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-11-26 06:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='First_Menu',
            fields=[
                ('nid', models.AutoField(primary_key=True, serialize=False, verbose_name='编号')),
                ('title', models.CharField(max_length=30, unique=True, verbose_name='顶级菜单')),
                ('ico', models.CharField(default='menu-icon fa fa-caret-right', max_length=40, verbose_name='图标')),
                ('status', models.BooleanField(default=True, verbose_name='状态')),
                ('remark', models.CharField(max_length=100, null=True, verbose_name='备注')),
            ],
        ),
        migrations.CreateModel(
            name='Second_Menu',
            fields=[
                ('nid', models.AutoField(primary_key=True, serialize=False, verbose_name='编号')),
                ('title', models.CharField(max_length=30, verbose_name='二级菜单')),
                ('url', models.CharField(default=None, max_length=40, verbose_name='链接')),
                ('ico', models.CharField(default='menu-icon fa fa-caret-right', max_length=40, verbose_name='图标')),
                ('status', models.BooleanField(default=True, verbose_name='状态')),
                ('remark', models.CharField(max_length=100, null=True, verbose_name='备注')),
                ('first_menu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='menu_management.First_Menu')),
            ],
        ),
    ]
