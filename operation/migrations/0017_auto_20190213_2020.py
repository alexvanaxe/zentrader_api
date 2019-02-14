# Generated by Django 2.1.5 on 2019-02-13 20:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0016_auto_20190212_1950'),
    ]

    operations = [
        migrations.AlterField(
            model_name='operation',
            name='category',
            field=models.CharField(choices=[('DT', 'Daytrade'), ('O', 'Ordinary'), ('F', 'Fraction'), ('NA', 'Not yet Defined')], default='NA', max_length=2),
            preserve_default=False,
        ),
    ]