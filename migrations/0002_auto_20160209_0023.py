# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-09 00:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('osugraphs', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mapinfo',
            name='beatmap_id',
            field=models.IntegerField(unique=True),
        ),
        migrations.AlterField(
            model_name='mapinfo',
            name='max_combo',
            field=models.IntegerField(null=True),
        ),
    ]
