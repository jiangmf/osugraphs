import json, datetime, pycountry, time, pytz

from urllib.request import urlopen
from django.db import models
#from django_cron import CronJobBase, Schedule
from django.core.mail import send_mail

from osugraphs.settings import OSU_API_KEY as _key
from osugraphs.util import print_json, pprint

from bs4 import BeautifulSoup

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
                    artist = data['artist'],
                    title  = data['title'],
                    bpm = data['bpm'],
                    difficultyrating = data['difficultyrating'],
                    diff_size = data['diff_size'],
                    diff_overall =data['diff_overall'],
                    diff_approach = data['diff_approach'],
                    diff_drain = data['diff_drain'],
                    hit_length = data['hit_length'],
                    version = data['title'],
                    max_combo = data['max_combo']
                )

            score['map_info'] = map_info
            try:
                score_obj = Score.objects.get(user=user, map_info=map_info)
                print(score_obj.date)
                print(score['date']) 
                if (score_obj.date.year   == score['date'].year   and
                    score_obj.date.month  == score['date'].month  and
                    score_obj.date.day    == score['date'].day    and
                    score_obj.date.hour   == score['date'].hour   and
                    score_obj.date.minute == score['date'].minute and
                    score_obj.date.second == score['date'].second) :
                    continue
                    print("SKIPPED CREATING SCORE")
                else:
                    score_obj.update(**score)
                    score_obj.save()
                    print("UPDATED SCORE")
            except Score.DoesNotExist:
                Score.objects.create(**score)

def get_beatmap_data(since="2000-01-01"):
    response = urlopen(
        'https://osu.ppy.sh/api/get_beatmaps?k={0}&since={1}'.format(_key, since)
    )
    data = json.loads(response.readall().decode('utf-8'))

    for bmap in data:
        # print_json(bmap)

        bmap['approved_date'] = datetime.datetime.strptime(bmap['approved_date'], '%Y-%m-%d %H:%M:%S').replace(tzinfo=pytz.utc)
        bmap['last_update'] = datetime.datetime.strptime(bmap['last_update'], '%Y-%m-%d %H:%M:%S').replace(tzinfo=pytz.utc)

        # pprint(bmap)
        beatmap_id = bmap.pop('beatmap_id')
        map_info, created = MapInfo.objects.update_or_create(beatmap_id=beatmap_id, defaults=bmap)
        if created: 
            print("Created Map ID {0}".format(map_info.beatmap_id))

def get_beatmap_datas():
    day = datetime.date(2007,10,7)
    while day < datetime.datetime.today().date():
        print("===========================================================")
        print(day.strftime("%Y-%m-%d"))
        print("===========================================================")
        get_beatmap_data(day.strftime("%Y-%m-%d"))
        day = day + datetime.timedelta(days=3)
        time.sleep(0.5)

def get_players():
    response = urlopen('https://osu.ppy.sh/p/pp/?m=0&s=3&o=1&f=0&page=2')
    html = response.read()
    soup = BeautifulSoup(html, 'html.parser')

    for tr in soup.find_all(class_="beatmapListing")[0].find_all('tr'):
        try:
            player_name = tr.find_all('a')[0].decode_contents(formatter="html")
            print(player_name)

            response = urlopen(
                'https://osu.ppy.sh/api/get_user?k={0}&u={1}'.format(_key, player_name)
            )
            data = json.loads(response.readall().decode('utf-8'))
            player, created = User.objects.update_or_create(id=data[0]['user_id'], defaults={
                "name" : data[0]['username'],
                "country" : data[0]['country'],
            })
            if created: 
                print("Created Player {0}".format(player))
        except:
            import traceback; traceback.print_exc()
            # print(tr)

def get_user(user_id):
    get_data(user_id)
    get_scores(user_id)