# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-26 19:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('confabulation', '0003_auto_20170326_1858'),
    ]

    operations = [
        migrations.AddField(
            model_name='story',
            name='notes',
            field=models.TextField(blank=True, null=True),
        ),
    ]
