# Generated by Django 2.2 on 2019-04-19 08:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('confabulation', '0014_connection_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chain',
            name='connection_range',
            field=models.CharField(choices=[('Inter-connection', 'interconection'), ('Intra-connection', 'intraconnection')], max_length=30),
        ),
        migrations.AlterField(
            model_name='connection',
            name='connection_range',
            field=models.CharField(choices=[('Inter-connection', 'interconection'), ('Intra-connection', 'intraconnection')], max_length=30),
        ),
        migrations.AlterField(
            model_name='storytostoryconnection',
            name='connection_range',
            field=models.CharField(choices=[('Inter-connection', 'interconection'), ('Intra-connection', 'intraconnection')], max_length=30),
        ),
        migrations.AlterField(
            model_name='theme',
            name='connection_range',
            field=models.CharField(choices=[('Inter-connection', 'interconection'), ('Intra-connection', 'intraconnection')], max_length=30),
        ),
    ]
