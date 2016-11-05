# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-11-04 18:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('qa', '0009_auto_20161104_1816'),
        ('users', '0002_auto_20161013_0207'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='level',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='qa.Level'),
        ),
    ]
