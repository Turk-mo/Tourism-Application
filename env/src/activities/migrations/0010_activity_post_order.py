# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2019-04-24 08:13
from __future__ import unicode_literals

import activities.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0009_auto_20190424_0906'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='post_order',
            field=activities.fields.PositionField(default=-1),
        ),
    ]
