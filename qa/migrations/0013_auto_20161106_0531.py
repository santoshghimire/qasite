# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-11-06 05:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qa', '0012_auto_20161106_0527'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quizresult',
            name='obtained_score',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='quizresult',
            name='total_score',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
