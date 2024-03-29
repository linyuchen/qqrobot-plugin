# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-09 04:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AdminUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qq', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='GlobalSetting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('robot_name', models.CharField(max_length=20)),
                ('admins', models.ManyToManyField(to='globalconf.AdminUser')),
            ],
        ),
    ]
