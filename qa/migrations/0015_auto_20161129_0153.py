# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-29 01:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qa', '0014_auto_20161111_0905'),
    ]

    operations = [
        migrations.AlterField(
            model_name='level',
            name='name',
            field=models.IntegerField(help_text='Enter the level name', verbose_name='name'),
        ),
    ]
