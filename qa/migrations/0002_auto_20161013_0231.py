# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-13 02:31
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('qa', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='article',
            old_name='article',
            new_name='category',
        ),
    ]
