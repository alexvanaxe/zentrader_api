# Generated by Django 3.0.6 on 2020-06-02 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trade_system', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='analysis',
            name='beginning',
        ),
        migrations.RemoveField(
            model_name='analysis',
            name='end',
        ),
        migrations.AddField(
            model_name='analysis',
            name='tunnel_bottom',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=22, null=True, verbose_name='Bottom tunnel'),
        ),
        migrations.AddField(
            model_name='analysis',
            name='tunnel_top',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=22, null=True, verbose_name='Top tunnel'),
        ),
    ]
