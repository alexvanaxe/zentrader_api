# Generated by Django 2.0.6 on 2018-07-15 19:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='buydata',
            name='stop_gain',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=22, null=True, verbose_name='stop gain'),
        ),
        migrations.AddField(
            model_name='buydata',
            name='stop_loss',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=22, null=True, verbose_name='stop loss'),
        ),
    ]
