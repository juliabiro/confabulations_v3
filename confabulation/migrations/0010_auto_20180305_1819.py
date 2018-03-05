# Generated by Django 2.0.2 on 2018-03-05 18:19

import colorful.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('confabulation', '0009_auto_20180305_1328'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='story',
            name='keywords',
        ),
        migrations.AddField(
            model_name='story',
            name='keywords',
            field=models.ManyToManyField(blank=True, null=True, to='confabulation.Keyword'),
        ),
    ]