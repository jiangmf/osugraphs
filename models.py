import json, datetime, pycountry

from urllib.request import urlopen
from django.db import models
from django_cron import CronJobBase, Schedule
from django.core.mail import send_mail

from osugraphs.settings import OSU_API_KEY as _key
from osugraphs.util import print_json


class User(models.Model):
    name = models.CharField(max_length=50)
    id = models.IntegerField(primary_key=True)
    country = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    @property
    def country_name(self):
        return pycountry.countries.get(alpha2=self.country).name

class DataPoint(models.Model):
    user = models.ForeignKey(User, related_name='data_point_set')
    time = models.DateTimeField(default=datetime.datetime.now)

    count300 = models.IntegerField()
    count100 = models.IntegerField()
    count50 = models.IntegerField()
    playcount = models.IntegerField()
    ranked_score = models.BigIntegerField()
    total_score = models.BigIntegerField()
    pp_rank = models.IntegerField()
    level = models.FloatField()
    pp_raw = models.FloatField()
    accuracy = models.FloatField()
    count_rank_ss = models.IntegerField()
    count_rank_s = models.IntegerField()
    count_rank_a = models.IntegerField()
    pp_country_rank = models.IntegerField()

class Score(models.Model):
    user = models.ForeignKey(User, related_name='score_set')
    

    score = models.IntegerField()
    maxcombo = models.IntegerField()
    count300 = models.IntegerField()
    count100 = models.IntegerField()
    count50 = models.IntegerField()
    countmiss = models.IntegerField()
    countkatu = models.IntegerField()
    countgeki = models.IntegerField()
    perfect = models.BooleanField()
    enabled_mods = models.IntegerField()
    date = models.DateTimeField()
    rank = models.CharField(max_length=5)
    pp = models.FloatField()

    map_info = models.ForeignKey('MapInfo', related_name='score_set')

    @property
    def static_rank_png(self):
        return "img/rank/{0}.png".format(self.rank)
    @property
    def mods(self):
        # TODO: REWORK THIS
        if self.enabled_mods == 0:
            return "None"
        elif self.enabled_mods == 8:
            return "HD"
        elif self.enabled_mods == 16:
            return "HR"
        elif self.enabled_mods == 24:
            return "HDHR"
        elif self.enabled_mods == 64:
            return "DT"
        elif self.enabled_mods == 72:
            return "HDDT"
        elif self.enabled_mods == 576:
            return "NC"
        elif self.enabled_mods == 584:
            return "HDNC"

class MapInfo(models.Model):
    beatmap_id = models.IntegerField()
    artist = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    bpm = models.FloatField()
    difficultyrating = models.FloatField()
    diff_size = models.FloatField()
    diff_overall = models.FloatField()
    diff_approach = models.FloatField()
    diff_drain = models.FloatField()
    hit_length = models.FloatField()
    version = models.CharField(max_length=255)