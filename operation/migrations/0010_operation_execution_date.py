# Generated by Django 2.0.6 on 2018-12-03 17:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0009_auto_20181130_1737'),
    ]

    operations = [
        migrations.AddField(
            model_name='operation',
            name='execution_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='execution date'),
        ),
    ]
