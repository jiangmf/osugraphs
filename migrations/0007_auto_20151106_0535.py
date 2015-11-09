# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('osugraphs', '0006_auto_20151031_0445'),
    ]

    operations = [
        migrations.AddField(
            model_name='mapinfo',
            name='bpm',
            field=models.FloatField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='mapinfo',
            name='diff_approach',
            field=models.FloatField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='mapinfo',
            name='diff_drain',
            field=models.FloatField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='mapinfo',
            name='diff_overall',
            field=models.FloatField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='mapinfo',
            name='diff_size',
            field=models.FloatField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='mapinfo',
            name='difficultyrating',
            field=models.FloatField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='mapinfo',
            name='hit_length',
            field=models.FloatField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='mapinfo',
            name='version',
            field=models.CharField(max_length=255, default=1),
            preserve_default=False,
        ),
    ]
