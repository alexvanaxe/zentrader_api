# Generated by Django 2.0.6 on 2018-07-02 21:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_auto_20180702_2103'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='next_account',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='account.Account'),
        ),
    ]
