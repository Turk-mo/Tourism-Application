# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2019-04-21 01:14
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_post_latest_update'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='embed_code',
            new_name='embed_link',
        ),
    ]