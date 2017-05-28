# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-28 18:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0013_auto_20170525_0254'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='comment',
        ),
        migrations.AddField(
            model_name='post',
            name='comments',
            field=models.ManyToManyField(related_name='comments_to_post', to='home.comment'),
        ),
    ]
