from django.shortcuts import render
from pages.models import Anime, Episodes
from account.models import *
from django.contrib.sites.shortcuts import get_current_site
# Create your views here.
def anime(request, slug):
    if not Anime.objects.filter(name=slug.replace('-',' ')).exists():
        return render(request, 'pages/error404.html') 
    domain = get_current_site(request)
    class_fav = ''
    anime = Anime.objects.get(name=slug.replace('-',' '))
    anime.url_anime = anime.name.replace(' ','-')
    episodes = Episodes.objects.filter(name=anime).order_by('episode')
    class_done = ''
    if request.user.is_authenticated:
        if UsersBack.objects.filter(user=request.user, animes_fav=anime):
            class_fav = 'favorite'
        if done_show.objects.filter(user=request.user, animes=anime).exists():
            class_done = 'favorite'

    for i in episodes:
        i.video = i.name.name.replace(' ','-')

    genre = anime.anime_class.all() 
    for i in genre:
        i.url_genre = i.name.replace(' ','-')



    x = {
        'anime' : anime,
        'class' : genre,
        'title' : anime.name.title(),
        'episodes': episodes,
        'class_fav': class_fav,
        'class_done': class_done,
        'domain': domain,
    }

    return render(request, 'pages/anime-profile.html', x)

def watch(request, slug, eps_num):
    if not Anime.objects.filter(name=slug.replace('-', ' ')).exists():
        return render(request, 'pages/error404.html')
    domain = get_current_site(request)
    anime = Anime.objects.get(name=slug.replace('-',' '))
    if not Episodes.objects.filter(name=anime, episode=str(eps_num)).exists():
        return render(request, 'pages/error404.html')

    episodes = Episodes.objects.filter(name=anime).order_by('episode')

    episode = Episodes.objects.get(name=anime, episode=str(eps_num))
    episode.title = episode.name.name.title()
    
    m = 'hide'
    n = 'hide'
    
    nex = episodes.filter(episode__gte=int(eps_num))
    prvg = episodes.filter(episode__lte=int(eps_num))

    if len(nex) > 1:
        n = nex[1]
        n.url_anime = n.name.name.replace(' ','-')
    
    if len(prvg) > 1:
        m = list(prvg)[-2]
        m.url_anime = m.name.name.replace(' ','-')


    for i in episodes:
        i.url_anime = i.name.name.replace(' ','-')
    
    x = {
        'episode': episode,
        'episodes': episodes,
        'prv_hide': m,
        'next_hide': n,
        'domain': domain,
    }
    return render(request, 'pages/watch.html', x)

def error404(request, exception):
    return render(request, 'pages/error404.html')

def error500(request, *args, **argv):
    return render(request, 'errors/error500.html')
    
def error403(request, *args, **argv):
    return render(request, 'errors/error403.html')