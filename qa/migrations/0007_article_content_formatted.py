# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-11-03 02:03
from __future__ import unicode_literals

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('qa', '0006_auto_20161103_0154'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='content_formatted',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True),
        ),
    ]
