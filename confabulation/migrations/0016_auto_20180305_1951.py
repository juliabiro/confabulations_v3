# Generated by Django 2.0.2 on 2018-03-05 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('confabulation', '0015_auto_20180305_1951'),
    ]

    operations = [
        migrations.CreateModel(
            name='Keywords',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ],
        ),
    ]
