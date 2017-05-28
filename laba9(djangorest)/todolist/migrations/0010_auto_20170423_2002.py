# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-23 20:02
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('todolist', '0009_auto_20170422_1651'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tasklist',
            name='owner',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='lists', to=settings.AUTH_USER_MODEL),
        ),
    ]
