# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-05-19 05:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='password',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
    ]
