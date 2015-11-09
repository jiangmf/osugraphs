# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('osugraphs', '0003_auto_20151027_2300'),
    ]

    operations = [
        migrations.AddField(
            model_name='score',
            name='beatmap_id',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
