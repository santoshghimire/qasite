# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-11-11 09:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('qa', '0013_auto_20161106_0531'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='active',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='article',
            name='created',
            field=model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created'),
        ),
        migrations.AddField(
            model_name='article',
            name='modified',
            field=model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified'),
        ),
    ]
