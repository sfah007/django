from django.shortcuts import render
from pages.models import Anime, Episodes
from account.models import *
# Create your views here.
def anime(request, slug):
    if not Anime.objects.filter(name=slug.replace('-',' ')).exists():
        return render(request, 'pages/error404.html') 
    class_fav = ''
    anime = Anime.objects.get(name=slug.replace('-',' '))
    anime.url_anime = anime.name.replace(' ','-')
    episodes = Episodes.objects.filter(name=anime).order_by('episode')

    if request.user.is_authenticated:
        if UsersBack.objects.filter(user=request.user, animes_fav=anime):
            class_fav = 'favorite'

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
        'episodes': episodes,
        'class_fav': class_fav,
    }

    return render(request, 'pages/anime-profile.html', x)

def watch(request, slug, eps_num):
    if not Anime.objects.filter(name=slug.replace('-', ' ')).exists():
        return render(request, 'pages/error404.html')

    anime = Anime.objects.get(name=slug.replace('-',' '))
    if not Episodes.objects.filter(name=anime, episode=str(eps_num)).exists():
        return render(request, 'pages/error404.html')

    episodes = Episodes.objects.filter(name=anime).order_by('episode')


    episode = Episodes.objects.get(name=anime, episode=str(eps_num))
    m = 'hide'
    n = 'hide'

    if episodes.filter(episode=str(int(eps_num)-1)).exists():
        m = episodes.get(episode=str(int(eps_num)-1))
        m.url_anime = m.name.name.replace(' ','-')

    if episodes.filter(episode=str(int(eps_num)+1)).exists():
        n = episodes.get(episode=str(int(eps_num)+1))
        n.url_anime = n.name.name.replace(' ','-')

    
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

def error500(request, *args, **argv):
    return render(request, 'pages/error404.html')