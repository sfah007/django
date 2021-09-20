from django.shortcuts import render
from pages.models import Anime, Episodes
# Create your views here.
def anime(request, slug):
    anime = Anime.objects.get(name=slug.replace('-',' '))
    episodes = Episodes.objects.filter(name=anime).order_by('episode')

    for i in episodes:
        i.video = i.name.name.replace(' ','-')

    animes = Anime.objects.all()
    for i in animes:
        i.url_anime = i.name.replace(' ','-')
        i.title = i.name.title()

    x = {
        'anime' : anime,
        'class' : anime.anime_class.all(),
        'title' : anime.name.title(),
        'episodes': episodes
    }

    return render(request, 'pages/anime-profile.html', x)

def watch(request, slug, eps_num):
    anime = Anime.objects.get(name=slug.replace('-',' '))
    episodes = Episodes.objects.filter(name=anime).order_by('episode')

    episode = Episodes.objects.get(name=anime, episode=str(eps_num))
    e = float(episode.episode)

    m = Episodes.objects.get(name=anime, episode=str(eps_num))
    m.episode = -100000
    n = Episodes.objects.get(name=anime, episode=str(eps_num))
    n.episode = 100000
    for i in episodes:
        v1 = float(i.episode)
        if v1 < e and v1 > float(m.episode):
            m = i
        if v1 > e and v1 < float(n.episode):
            n = i
    
    print('M : ',m)
    if m.episode == -100000:
        m = 'hide'
    else:
        m.name.name = m.name.name.replace(' ', '-')

    if n.episode == 100000:
        n = 'hide'
    else:
        n.name.name = n.name.name.replace(' ', '-')

    animes = Anime.objects.all()
    for i in animes:
        i.url_anime = i.name.replace(' ','-')
        i.title = i.name.title()

    for i in episodes:
        i.url_anime = i.name.name.replace(' ','-')

    x = {
        'episode': episode,
        'episodes': episodes,
        'animes_search': animes,
        'prv_hide': m,
        'next_hide': n,
    }
    return render(request, 'pages/watch.html', x)

def error404(request, exception):
    return render(request, 'pages/error404.html')