import requests, json, time
from bs4 import BeautifulSoup
from collections import OrderedDict
from osugraphs.models import User, DataPoint, Score, MapInfo
import random

MODS = OrderedDict([
    ("NF"       , 0b00000000000000000000000000001),
    ("EZ"       , 0b00000000000000000000000000010),
    ("No Video" , 0b00000000000000000000000000100),
    ("HD"       , 0b00000000000000000000000001000),
    ("HR"       , 0b00000000000000000000000010000),
    ("SD"       , 0b00000000000000000000000100000),
    ("DT"       , 0b00000000000000000000001000000),
    ("RX"       , 0b00000000000000000000010000000),
    ("HT"       , 0b00000000000000000000100000000),
    ("NC"       , 0b00000000000000000001000000000),
    ("FL"       , 0b00000000000000000010000000000),
    ("Autoplay" , 0b00000000000000000100000000000),
    ("SO"       , 0b00000000000000001000000000000),
    ("AP"       , 0b00000000000000010000000000000),
    ("PF"       , 0b00000000000000100000000000000),
    ("K4"       , 0b00000000000001000000000000000),
    ("K5"       , 0b00000000000010000000000000000),
    ("K6"       , 0b00000000000100000000000000000),
    ("K7"       , 0b00000000001000000000000000000),
    ("K8"       , 0b00000000010000000000000000000),
    ("FI"       , 0b00000000100000000000000000000),
    ("Random"   , 0b00000001000000000000000000000),
    ("LastMod"  , 0b00000010000000000000000000000),
    ("K9"       , 0b00001000000000000000000000000),
    ("K10"      , 0b00010000000000000000000000000),
    ("K1"       , 0b00100000000000000000000000000),
    ("K3"       , 0b01000000000000000000000000000),
    ("K2"       , 0b10000000000000000000000000000),
])

class OsuAPI(object):
    ROOT_URL = "https://osu.ppy.sh/api/"

    def __init__(self, api_key=None):
        self.api_key = api_key

    '''
    Utility
    '''
    def clean_response(self, r):
        return json.loads(r.text)

    def get_params(self, params):
        return {k: v for k, v in params.items() if v is not None}

    def request(self, method, **kwargs):
        i = random.randint(0,100)
        if i == 0:
            time.sleep(0.5)
        if 'params' in kwargs:
            kwargs['params'].update({"k": self.api_key})
        r = requests.get(self.ROOT_URL + method, **kwargs)
        return self.clean_response(r)

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
    
    def get_osu_direct_link(self, map_set_id):
        return "osu://dl/{}",format(map_set_id)

    def get_blood_cat_link(self, map_set_id):
        return "http://bloodcat.com/osu/s/{}".format(map_set_id)

    def get_user_profile_image(self, user_id):
        response = requests.get('https://osu.ppy.sh/u/{}'.format(user_id)).text
        # html = response.read()
        soup = BeautifulSoup(response, 'html.parser')
        return "https:" + soup.find_all(class_="avatar-holder")[0].find_all('img')[0].get('src')

    def get_players(self, page=None):
        response = requests.get('https://osu.ppy.sh/p/pp/?m=0&s=3&o=1&f=0&page={}'.format(page)).text
        # html = response.read()
        soup = BeautifulSoup(response, 'html.parser')

        for tr in soup.find_all(class_="beatmapListing")[0].find_all('tr'):
            try:
                player_name = tr.find_all('a')[0].decode_contents(formatter="html")
                
                data = self.get_user(u=player_name)

                player, created = User.objects.update_or_create(id=data[0]['user_id'], defaults={
                    "name" : data[0]['username'],
                    "country" : data[0]['country'],
                })
                if created: 
                    print("Created Player {0}".format(player))
            except:
                import traceback; traceback.print_exc()

    '''
    API methods
    '''

    def get_user(self, u, m=None, type=None, event_days=None):
        params = self.get_params(locals())
        return self.request('get_user', params=params)

    def get_beatmaps(self, since=None, s=None, b=None, u=None, type=None, m=None, a=None, h=None, limit=None):
        params = self.get_params(locals())
        return self.request('get_beatmaps', params=params)

    def get_scores(self, b, u=None, m=None, mods=None, type=None, limit=None):
        params = self.get_params(locals())
        return self.request('get_beatmaps', params=params)

    def get_user_best(self, u, m=None, limit=None, type=None):
        params = self.get_params(locals())
        return self.request('get_user_best', params=params)

    def get_user_recent(self, u, m=None, limit=None, type=None):
        params = self.get_params(locals())
        return self.request('get_user_best', params=params)

    def get_match(self, mp):
        params = self.get_params(locals())
        return self.request('get_match', params=params)

    def get_replay(self, k, m, b, u):
        params = self.get_params(locals())
        return self.request('get_replay', params=params)        