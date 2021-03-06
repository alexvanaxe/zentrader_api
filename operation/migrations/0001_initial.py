# Generated by Django 2.1.5 on 2019-06-14 14:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('stock', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Operation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(editable=False, verbose_name='creation date')),
                ('execution_date', models.DateTimeField(blank=True, null=True, verbose_name='execution date')),
                ('amount', models.DecimalField(decimal_places=0, max_digits=22, verbose_name='amount')),
                ('price', models.DecimalField(decimal_places=2, max_digits=22, verbose_name='stock value')),
                ('category', models.CharField(choices=[('DT', 'Daytrade'), ('O', 'Ordinary'), ('F', 'Fraction'), ('NA', 'Not yet Defined')], default='NA', max_length=2)),
                ('archived', models.BooleanField(default=False, verbose_name='archived')),
                ('executed', models.BooleanField(default=False, verbose_name='executed')),
                ('nickname', models.TextField(blank=True, max_length=100, null=True, verbose_name='nickname')),
                ('favorite', models.IntegerField(default=0, verbose_name='favorite')),
            ],
        ),
        migrations.CreateModel(
            name='SellData',
            fields=[
                ('operation_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='operation.Operation')),
                ('stop_gain', models.DecimalField(blank=True, decimal_places=2, max_digits=22, null=True, verbose_name='stop gain')),
                ('stop_loss', models.DecimalField(blank=True, decimal_places=2, max_digits=22, null=True, verbose_name='stop loss')),
            ],
            bases=('operation.operation',),
            managers=[
                ('solds', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AddField(
            model_name='operation',
            name='account',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.Account'),
        ),
        migrations.AddField(
            model_name='operation',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='operations', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='operation',
            name='stock',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stock.Stock'),
        ),
    ]
