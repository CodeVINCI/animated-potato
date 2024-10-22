# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-04 13:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20170403_1610'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='image',
            field=models.ImageField(blank=True, upload_to='profile_pictures'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='description',
            field=models.TextField(blank=True, default='', max_length=300),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='location',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='website',
            field=models.URLField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='workAndemployment',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
    ]
