import json, datetime, pycountry, time, pytz

from urllib.request import urlopen
from django.db import models
#from django_cron import CronJobBase, Schedule
from django.core.mail import send_mail

from osugraphs.settings import OSU_API_KEY
from osugraphs.util import print_json, pprint

from bs4 import BeautifulSoup

def get_mod_combination(self, mod):
        if mod == 0:
            return ["None"]
        elif mod == 576:
            return ["NC"]

        ret = []
        for k, v in MODS.items():
            if mod & v:
                ret.append(k)

        return ret

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

    @property
    def percent300(self):
        return round(self.count300/(self.count300+self.count100+self.count50)*100,2)

    @property
    def percent100(self):
        return round(self.count100/(self.count300+self.count100+self.count50)*100,2)

    @property
    def percent50(self):
        return round(self.count50/(self.count300+self.count100+self.count50)*100,2)
    

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
        # # TODO: REWORK THIS
        # if self.enabled_mods == 0:
        #     return "None"
        # elif self.enabled_mods == 8:
        #     return "HD"
        # elif self.enabled_mods == 16:
        #     return "HR"
        # elif self.enabled_mods == 24:
        #     return "HDHR"
        # elif self.enabled_mods == 64:
        #     return "DT"
        # elif self.enabled_mods == 72:
        #     return "HDDT"
        # elif self.enabled_mods == 576:
        #     return "NC"
        # elif self.enabled_mods == 584:
        #     return "HDNC"

        # binary = [int(x) for x in bin(self.enabled_mods)[2:]]

        return "".join(get_mod_combination(self.enabled_mods))


    @property
    def accuracy(self):
        return round(
            (self.count300*6 + self.count100*2 + self.count50*1)/
            (self.count300*6 + self.count100*6 + self.count50*6 + self.countmiss*6)*100,2)
    

class MapInfo(models.Model):
    approved = models.IntegerField()
    approved_date = models.DateTimeField()
    last_update = models.DateTimeField()

    artist = models.CharField(max_length=255)
    
    beatmap_id = models.IntegerField(unique=True)
    beatmapset_id = models.IntegerField()
    
    bpm = models.FloatField()
    creator = models.CharField(max_length=255)
    difficultyrating = models.FloatField()
    
    diff_size = models.FloatField()
    diff_overall = models.FloatField()
    diff_approach = models.FloatField()
    diff_drain = models.FloatField()
    
    hit_length = models.FloatField()
    source = models.CharField(max_length=255)

    genre_id = models.IntegerField()
    language_id = models.IntegerField()
    favourite_count = models.IntegerField()

    title = models.CharField(max_length=255)
    total_length = models.IntegerField()
    version = models.CharField(max_length=255)
    file_md5 = models.CharField(max_length=255)

    mode = models.IntegerField()
    tags = models.TextField()

    playcount = models.IntegerField()
    passcount = models.IntegerField()
    max_combo = models.IntegerField(null=True)

    def __str__(self):
        return "{0} [{1}]".format(self.title, self.version)