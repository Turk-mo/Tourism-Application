# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2019-04-23 14:23
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0002_event'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='event',
            unique_together=set([('slug', 'activity')]),
        ),
    ]
