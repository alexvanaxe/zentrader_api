# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-12-19 16:38
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0004_selldata'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='selldata',
            name='buy',
        ),
        migrations.AddField(
            model_name='selldata',
            name='operation',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='operation.Operation'),
            preserve_default=False,
        ),
    ]