# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-17 04:24
from __future__ import unicode_literals

from django.db import migrations, models
import qa.validators


class Migration(migrations.Migration):

    dependencies = [
        ('qa', '0003_auto_20161017_0423'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='audio',
            field=models.FileField(blank=True, help_text='Maximum file size allowed is 5Mb', null=True, upload_to='article', validators=[qa.validators.validate_audio]),
        ),
        migrations.AlterField(
            model_name='article',
            name='content',
            field=models.FileField(blank=True, help_text='Maximum file size allowed is 5Mb', null=True, upload_to='article', validators=[qa.validators.validate_file]),
        ),
        migrations.AlterField(
            model_name='option',
            name='image',
            field=models.ImageField(blank=True, help_text='Maximum file size allowed is 2Mb', null=True, upload_to='answerImages', validators=[qa.validators.validate_image]),
        ),
    ]
