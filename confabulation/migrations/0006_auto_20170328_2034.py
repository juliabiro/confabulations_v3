# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-28 20:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('confabulation', '0005_auto_20170328_2031'),
    ]

    operations = [
        migrations.AlterField(
            model_name='analysistype',
            name='description',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='chain',
            name='description',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='recording',
            name='data_collection_circumstances',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='theme',
            name='description',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='transscription',
            name='text_eng',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='transscription',
            name='text_hu',
            field=models.TextField(blank=True, default=''),
        ),
    ]
