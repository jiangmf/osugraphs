from osugraphs.models import *
from osugraphs.settings import OSU_API_KEY
from osugraphs.osu_api import OsuAPI

osu_api = OsuAPI(OSU_API_KEY)

def get_data(user_id=None):
    query_set = [User.objects.get(id=user_id)] if user_id else User.objects.all()

    for user in query_set:
        data = osu_api.get_user(u=user.id)[0]
        
        data.pop("user_id")
        data.pop("username")
        data.pop("country")
        data.pop("events")
        data['user'] = user

        DataPoint.objects.create(**data)

def get_scores(user_id=None):
    query_set = [User.objects.get(id=user_id)] if user_id else User.objects.all()

    for user in query_set:
        data = osu_api.get_user_best(u=user.id, limit=100)

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

def get_user(user_id):
    get_data(user_id)
    get_scores(user_id)
