# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-27 16:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0002_auto_20170710_1255'),
    ]

    operations = [
        migrations.CreateModel(
            name='BuyData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('operation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='operation.Operation')),
            ],
        ),
    ]
