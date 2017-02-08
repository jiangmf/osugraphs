from osugraphs.models import *
from osugraphs.settings import OSU_API_KEY
from osugraphs.osu_api import OsuAPI

osu_api = OsuAPI(OSU_API_KEY)

def load_users_from_leaderboards():
    for page in range(5):
        osu_api.get_players(page=page)

def load_user_data_points(user_id=None):
	load_user_info(user_id)
	load_user_scores(user_id)

def load_user_info(user_id=None):
    query_set = [User.objects.get(id=user_id)] if user_id else User.objects.all()

    for i, user in enumerate(query_set):
        if i % 100 == 0:
            time.sleep(0.5)
        data = osu_api.get_user(u=user.id)[0]
        
        data.pop("user_id")
        data.pop("username")
        data.pop("country")
        data.pop("events")
        data['user'] = user

        DataPoint.objects.create(**data)
        print("Created DataPoint for {}".format(user))

def load_user_scores(user_id=None):
    query_set = [User.objects.get(id=user_id)] if user_id else User.objects.all()

    for i, user in enumerate(query_set):
        if i % 100 == 0:
            time.sleep(0.5)
        data = osu_api.get_user_best(u=user.id, limit=100)

        for score in data:
            score.pop("user_id")

            beatmap_id = int(score.pop('beatmap_id'))

            score['user'] = user
            score['date'] = datetime.datetime.strptime(score['date'], '%Y-%m-%d %H:%M:%S')
            
            try:
                map_info = MapInfo.objects.get(beatmap_id=beatmap_id)
                # print("SKIPPED MAPINFO REQUEST")
            except MapInfo.DoesNotExist:
                map_info = load_beatmap_data(beatmap_id=beatmap_id)

            score['map_info'] = map_info

            try:
                score_obj = Score.objects.get(user=user, map_info=map_info)
                if (score_obj.date.year   == score['date'].year   and
                    score_obj.date.month  == score['date'].month  and
                    score_obj.date.day    == score['date'].day    and
                    score_obj.date.hour   == score['date'].hour   and
                    score_obj.date.minute == score['date'].minute and
                    score_obj.date.second == score['date'].second) :
                    # print(score['pp'], " SKIPPED CREATING SCORE ",map_info.title)

                    continue
                else:
                    Score.objects.filter(pk=score_obj.pk).update(**score)
                    # print(score['pp'], "UPDATED SCORE ", map_info.title)
            except Score.DoesNotExist:
                # print(score['pp'], "CREATING SCORE ", map_info.title)
                Score.objects.create(**score)

def load_beatmap_data(since=None, beatmap_id=None):
    if since:
        data = osu_api.get_beatmaps(since=since)
    if beatmap_id:
        data = osu_api.get_beatmaps(b=beatmap_id)

    last_bmap_date = datetime.date(1900,1,1)

    for bmap in data:
        bmap['approved_date'] = datetime.datetime.strptime(bmap['approved_date'], '%Y-%m-%d %H:%M:%S').replace(tzinfo=pytz.utc)
        bmap['last_update'] = datetime.datetime.strptime(bmap['last_update'], '%Y-%m-%d %H:%M:%S').replace(tzinfo=pytz.utc)

        if bmap['approved_date'].date() > last_bmap_date:
            last_bmap_date = bmap['approved_date'].date()

        beatmap_id = bmap.pop('beatmap_id')

        map_info, created = MapInfo.objects.update_or_create(beatmap_id=beatmap_id, defaults=bmap)
        if created: 
            print("Created Map ID {0}".format(map_info.beatmap_id))

    if since:
        return last_bmap_date
    if beatmap_id:
        return map_info

def load_all_beatmaps():
    day = datetime.date(2007,10,7)
    while day < datetime.datetime.today().date():
        print("===========================================================")
        print(day.strftime("%Y-%m-%d"))
        print("===========================================================")
        last_bmap_date = load_beatmap_data(since=day.strftime("%Y-%m-%d"))
        day = last_bmap_date - datetime.timedelta(days=1)
        time.sleep(0.5)