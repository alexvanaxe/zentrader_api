# Generated by Django 2.1.5 on 2019-06-14 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=10, verbose_name='Code')),
                ('name', models.CharField(max_length=140, verbose_name='Name')),
                ('sector', models.CharField(blank=True, max_length=140, null=True, verbose_name='Sector')),
                ('subsector', models.CharField(blank=True, max_length=140, null=True, verbose_name='Subsector')),
                ('price', models.DecimalField(decimal_places=2, max_digits=22, verbose_name='stock value')),
            ],
        ),
    ]
