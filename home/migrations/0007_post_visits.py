# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-22 19:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_auto_20170520_0553'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='visits',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
