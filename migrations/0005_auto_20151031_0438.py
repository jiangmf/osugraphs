# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('osugraphs', '0004_score_beatmap_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='MapInfo',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('beatmap_id', models.IntegerField()),
                ('artist', models.CharField(max_length=50)),
                ('title', models.CharField(max_length=255)),
            ],
        ),
        migrations.RemoveField(
            model_name='score',
            name='beatmap_id',
        ),
        migrations.AddField(
            model_name='score',
            name='map_info',
            field=models.ForeignKey(default=1, to='osugraphs.MapInfo', related_name='score_set'),
            preserve_default=False,
        ),
    ]
