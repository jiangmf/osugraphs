# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('osugraphs', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datapoint',
            name='ranked_score',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='datapoint',
            name='total_score',
            field=models.BigIntegerField(),
        ),
    ]
