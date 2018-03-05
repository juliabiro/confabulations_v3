# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-28 20:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('confabulation', '0004_auto_20170328_2027'),
    ]

    operations = [
        migrations.AlterField(
            model_name='analysispoint',
            name='description',
            field=models.CharField(blank=True, max_length=2000, null=True),
        ),
        migrations.AlterField(
            model_name='analysispoint',
            name='name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='analysistype',
            name='description',
            field=models.CharField(blank=True, max_length=2000, null=True),
        ),
        migrations.AlterField(
            model_name='analysistype',
            name='name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='chain',
            name='connection_range',
            field=models.CharField(choices=[(b'Interconnection', b'interconnection'), (b'Intraconnection', b'intraconnection')], max_length=30),
        ),
        migrations.AlterField(
            model_name='chain',
            name='description',
            field=models.CharField(blank=True, max_length=2000, null=True),
        ),
        migrations.AlterField(
            model_name='chain',
            name='name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='participant',
            name='gender',
            field=models.CharField(choices=[(b'female', b'female'), (b'male', b'male'), (b'other', b'other')], max_length=20),
        ),
        migrations.AlterField(
            model_name='participant',
            name='name',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='participant',
            name='participation_group',
            field=models.CharField(choices=[(b'non-photgrapher', b'non_photographer'), (b'photographer', b'photographer'), (b'student', b'student')], max_length=50),
        ),
        migrations.AlterField(
            model_name='photo',
            name='name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='recording',
            name='data_collection_circumstances',
            field=models.CharField(blank=True, max_length=2000, null=True),
        ),
        migrations.AlterField(
            model_name='recording',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='story',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='story',
            name='notes',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='storytostoryconnection',
            name='connection_range',
            field=models.CharField(choices=[(b'Interconnection', b'interconnection'), (b'Intraconnection', b'intraconnection')], max_length=30),
        ),
        migrations.AlterField(
            model_name='theme',
            name='connection_range',
            field=models.CharField(choices=[(b'Interconnection', b'interconnection'), (b'Intraconnection', b'intraconnection')], max_length=30),
        ),
        migrations.AlterField(
            model_name='theme',
            name='description',
            field=models.CharField(blank=True, max_length=2000, null=True),
        ),
        migrations.AlterField(
            model_name='theme',
            name='name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='transscription',
            name='text_eng',
            field=models.CharField(blank=True, max_length=10000, null=True),
        ),
        migrations.AlterField(
            model_name='transscription',
            name='text_hu',
            field=models.CharField(blank=True, max_length=10000, null=True),
        ),
    ]
