# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-10 01:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('globalconf', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='globalsetting',
            name='private_currency_name',
            field=models.CharField(default='\u91d1\u5e01', max_length=20),
        ),
    ]
