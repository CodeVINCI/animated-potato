# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-12 06:51
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0010_auto_20170512_0637'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='newspapers',
            new_name='newspaper',
        ),
        migrations.RenameField(
            model_name='following',
            old_name='newspapers',
            new_name='newspaper',
        ),
    ]
