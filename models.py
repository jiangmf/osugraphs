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

def get_data(user_id=None):
    if not user_id:
        query_set = User.objects.all()
    else:
        query_set = [User.objects.get(id=user_id)]
    for user in query_set:
        response = urlopen(
            'https://osu.ppy.sh/api/get_user?k={0}&u={1}'.format(_key, user.id)
            )
        data = json.loads(response.readall().decode('utf-8'))[0]
        
        data.pop("user_id")
        data.pop("username")
        data.pop("country")
        data.pop("events")
        data['user'] = user

        DataPoint.objects.create(**data)

def get_scores(user_id=None):
    if not user_id:
        query_set = User.objects.all()
    else:
        query_set = [User.objects.get(id=user_id)]
    for user in query_set:
        response = urlopen(
            'https://osu.ppy.sh/api/get_user_best?k={0}&u={1}&limit=100'.format(_key, user.id)
            )
        data = json.loads(response.readall().decode('utf-8'))

        for score in data:
            score.pop("user_id")
            beatmap_id = int(score.pop('beatmap_id'))
            score['user'] = user
            score['date'] = datetime.datetime.strptime(score['date'], '%Y-%m-%d %H:%M:%S')
            
            try:
                map_info = MapInfo.objects.get(beatmap_id = beatmap_id)
                print("SKIPPED MAPINFO REQUEST")
            except MapInfo.DoesNotExist:
                response = urlopen(
                    'https://osu.ppy.sh/api/get_beatmaps?k={0}&b={1}&m=0'.format(_key, beatmap_id)
                    )
                data = json.loads(response.readall().decode('utf-8'))[0]
                map_info = MapInfo.objects.create(
                    beatmap_id=beatmap_id, 
                    artist=data['artist'],
                    title=data['title'])

            score['map_info'] = map_info
            try:
                score_obj = Score.objects.get(user=user, map_info=map_info)
                print(score_obj.date)
                print(score['date'])
                if score_obj.date == score['date']:
                    continue
                    print("SKIPPED CREATING SCORE")
                else:
                    score_obj.update(**score)
                    score_obj.save()
                    print("UPDATED SCORE")
            except Score.DoesNotExist:
                Score.objects.create(**score)

def get_user(user_id):
    get_data(user_id)
    get_scores(user_id)
