# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-05-30 18:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0006_operation_archived'),
    ]

    operations = [
        migrations.AlterField(
            model_name='operation',
            name='archived',
            field=models.BooleanField(default=False, verbose_name='archived'),
        ),
    ]