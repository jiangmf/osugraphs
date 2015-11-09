# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DataPoint',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('time', models.DateTimeField()),
                ('count300', models.IntegerField()),
                ('count100', models.IntegerField()),
                ('count50', models.IntegerField()),
                ('playcount', models.IntegerField()),
                ('ranked_score', models.IntegerField()),
                ('total_score', models.IntegerField()),
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
            name='Score',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
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
