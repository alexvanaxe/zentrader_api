# Generated by Django 2.1.5 on 2019-06-21 17:23

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('operation', '0003_auto_20190621_1723'),
        ('buy', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SellData',
            fields=[
                ('operation_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='operation.Operation')),
                ('stop_gain', models.DecimalField(blank=True, decimal_places=2, max_digits=22, null=True, verbose_name='stop gain')),
                ('stop_loss', models.DecimalField(blank=True, decimal_places=2, max_digits=22, null=True, verbose_name='stop loss')),
                ('buy', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='buy.BuyData')),
            ],
            bases=('operation.operation',),
            managers=[
                ('solds', django.db.models.manager.Manager()),
            ],
        ),
    ]