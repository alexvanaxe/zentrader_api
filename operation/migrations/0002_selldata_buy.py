# Generated by Django 2.1.5 on 2019-06-14 14:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('operation', '0001_initial'),
        ('buy', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='selldata',
            name='buy',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='buy.BuyData'),
        ),
    ]
