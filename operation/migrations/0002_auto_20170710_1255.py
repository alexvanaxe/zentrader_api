# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-10 12:55
from __future__ import unicode_literals

from django.db import migrations


def forwards_func(apps, schema_editor):
    # We get the model from the versioned app registry;
    # if we directly import it, it'll be the wrong version
    operation_type = apps.get_model("operation", "OperationType")
    db_alias = schema_editor.connection.alias
    operation_type.objects.using(db_alias).bulk_create([
        operation_type(name="Experience"),
        operation_type(name="Buy"),
        operation_type(name="Sell"),
    ])


def reverse_func(apps, schema_editor):
    # forwards_func() creates two Country instances,
    # so reverse_func() should delete them.
    operation_type = apps.get_model("operation", "OperationType")
    db_alias = schema_editor.connection.alias
    operation_type.objects.using(db_alias).filter(name="Experience").delete()
    operation_type.objects.using(db_alias).filter(name="Buy").delete()
    operation_type.objects.using(db_alias).filter(name="Sell").delete()

class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(forwards_func, reverse_func),
    ]