# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-22 08:02
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_follower'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Follower',
            new_name='Following',
        ),
    ]
