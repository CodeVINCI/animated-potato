# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-07 02:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0017_auto_20170606_0006'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='category',
            field=models.CharField(default='general', max_length=500),
        ),
    ]
