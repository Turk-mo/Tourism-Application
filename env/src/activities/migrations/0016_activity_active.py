# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2019-04-25 09:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0015_auto_20190424_1412'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
