# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('osugraphs', '0005_auto_20151031_0438'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mapinfo',
            name='artist',
            field=models.CharField(max_length=255),
        ),
    ]
