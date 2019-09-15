# Generated by Django 1.11.13 on 2018-08-06 08:01
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ('mail', '0002_auto_20171026_1835'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mailtemplate',
            name='department',
        ),
        migrations.AlterField(
            model_name='mailtemplate',
            name='usage',
            field=models.CharField(blank=True, choices=[('new', 'New Device is created'), ('room', 'Room is changed'), ('owner', 'person currently lending is changed'), ('reminder', 'Reminder that device is still owned'), ('overdue', 'Reminder that device is overdue'), ('trashed', 'Device is trashed')], max_length=200, null=True, verbose_name='Usage'),
        ),
    ]
