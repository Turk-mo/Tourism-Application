# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-05-09 08:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0021_activity_post'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='example',
            field=models.CharField(default=1, max_length=45),
            preserve_default=False,
        ),
    ]
