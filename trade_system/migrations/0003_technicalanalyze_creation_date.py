# Generated by Django 3.0.6 on 2020-06-23 18:19

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trade_system', '0002_auto_20200602_1525'),
    ]

    operations = [
        migrations.AddField(
            model_name='technicalanalyze',
            name='creation_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 6, 23, 18, 19, 25, 902435), editable=False, verbose_name='creation date'),
            preserve_default=False,
        ),
    ]
