from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponse
from urllib.request import urlopen
from bs4 import BeautifulSoup

from osugraphs.models import *

def home_view(request, context={}):
    users = User.objects.all()
    context = {
        'users' : users.order_by('name'),
    }
    if request.method == "POST":
        print_json(request.POST)
        try:
            try:
                int(request.POST['search-query'])
                user = User.objects.get(Q(id=request.POST['search-query']) | Q(name__iexact=request.POST['search-query']))
            except:
                user = User.objects.get(Q(name__iexact=request.POST['search-query']))
            return redirect(reverse('profile', args=[user.id]))
        except:
            import traceback; traceback.print_exc()
    return render(request, 'index.html', context)

def profile_view(request, context={}, profile_id=None):
    user = User.objects.get(id=profile_id)
    datapoints = user.data_point_set.all()

    score_set = user.score_set.all().order_by('-pp').select_related('map_info')
    
    mods = [score.mods for score in score_set.all()]

    num_hr, num_hd, num_nomod, num_dt = 0, 0, 0, 0,

    response = urlopen('https://osu.ppy.sh/u/{0}'.format(user.id))
    html = response.read()
    soup = BeautifulSoup(html, 'html.parser')

    profile_picture = "https:" + soup.find_all(class_="avatar-holder")[0].find_all('img')[0].get('src')
    print(profile_picture)

    for mod in mods:
        if "HD" in str(mod):
            num_hd +=1
        if "HR" in str(mod):
            num_hr +=1
        if "DT" in str(mod) or "NC" in str(mod):
            num_dt +=1
        if "None" in str(mod):
            num_nomod +=1

    count_nomod , performance_nomod = 0, 0
    count_hd    , performance_hd = 0, 0
    count_hr    , performance_hr = 0, 0
    count_dt    , performance_dt = 0, 0


    for score in score_set:
        if "HD" in str(score.mods) and count_hd < 10:
            performance_hd = performance_hd + score.pp * pow(0.95, count_hd)
            count_hd += 1
            print("HD", performance_hd)
        if "HR" in str(score.mods) and count_hr < 10:
            performance_hr = performance_hr + score.pp * pow(0.95, count_hr)
            count_hr += 1
            print("HR", performance_hr)
        if ("DT" in str(score.mods) or "NC" in str(score.mods)) and count_dt < 10:
            performance_dt = performance_dt + score.pp * pow(0.95, count_dt)
            count_dt += 1
            print("DT", performance_dt)
        if "None" in str(score.mods) and count_nomod < 10:
            performance_nomod = performance_nomod + score.pp * pow(0.95, count_nomod)
            count_nomod += 1
            print("NOMOD", performance_nomod)


    context = {
        'user'             : user,
        'datapoints'       : datapoints,
        'current'          : datapoints.last(),
        'num_datapoints'   : datapoints.count,
        'last_updated'     : datapoints.last().time,
        'date_joined'      : datapoints.first().time,
        'static_flag'      : 'img/flags-32/{0}.png'.format(user.country_name),
        'scores'           : score_set,
        'num_hr'           : num_hr,
        'num_hd'           : num_hd,
        'num_dt'           : num_dt,
        'num_nomod'        : num_nomod,
        'profile_picture'  : profile_picture,
        'performance_nomod': performance_nomod,
        'performance_hd'   : performance_hd,
        'performance_hr'   : performance_hr,
        'performance_dt'   : performance_dt,

    }
    return render(request, 'profile.html', context)