# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('osugraphs', '0002_auto_20151027_2256'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datapoint',
            name='time',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
