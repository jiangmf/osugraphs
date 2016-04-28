# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DataPoint',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('time', models.DateTimeField(default=datetime.datetime.now)),
                ('count300', models.IntegerField()),
                ('count100', models.IntegerField()),
                ('count50', models.IntegerField()),
                ('playcount', models.IntegerField()),
                ('ranked_score', models.BigIntegerField()),
                ('total_score', models.BigIntegerField()),
                ('pp_rank', models.IntegerField()),
                ('level', models.FloatField()),
                ('pp_raw', models.FloatField()),
                ('accuracy', models.FloatField()),
                ('count_rank_ss', models.IntegerField()),
                ('count_rank_s', models.IntegerField()),
                ('count_rank_a', models.IntegerField()),
                ('pp_country_rank', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='MapInfo',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('approved', models.IntegerField()),
                ('approved_date', models.DateTimeField()),
                ('last_update', models.DateTimeField()),
                ('artist', models.CharField(max_length=255)),
                ('beatmap_id', models.IntegerField(unique=True)),
                ('beatmapset_id', models.IntegerField()),
                ('bpm', models.FloatField()),
                ('creator', models.CharField(max_length=255)),
                ('difficultyrating', models.FloatField()),
                ('diff_size', models.FloatField()),
                ('diff_overall', models.FloatField()),
                ('diff_approach', models.FloatField()),
                ('diff_drain', models.FloatField()),
                ('hit_length', models.FloatField()),
                ('source', models.CharField(max_length=255)),
                ('genre_id', models.IntegerField()),
                ('language_id', models.IntegerField()),
                ('favourite_count', models.IntegerField()),
                ('title', models.CharField(max_length=255)),
                ('total_length', models.IntegerField()),
                ('version', models.CharField(max_length=255)),
                ('file_md5', models.CharField(max_length=255)),
                ('mode', models.IntegerField()),
                ('tags', models.TextField()),
                ('playcount', models.IntegerField()),
                ('passcount', models.IntegerField()),
                ('max_combo', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Score',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('score', models.IntegerField()),
                ('maxcombo', models.IntegerField()),
                ('count300', models.IntegerField()),
                ('count100', models.IntegerField()),
                ('count50', models.IntegerField()),
                ('countmiss', models.IntegerField()),
                ('countkatu', models.IntegerField()),
                ('countgeki', models.IntegerField()),
                ('perfect', models.BooleanField()),
                ('enabled_mods', models.IntegerField()),
                ('date', models.DateTimeField()),
                ('rank', models.CharField(max_length=5)),
                ('pp', models.FloatField()),
                ('map_info', models.ForeignKey(to='osugraphs.MapInfo', related_name='score_set')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('name', models.CharField(max_length=50)),
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('country', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='score',
            name='user',
            field=models.ForeignKey(to='osugraphs.User', related_name='score_set'),
        ),
        migrations.AddField(
            model_name='datapoint',
            name='user',
            field=models.ForeignKey(to='osugraphs.User', related_name='data_point_set'),
        ),
    ]
