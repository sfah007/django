from django.shortcuts import render, get_object_or_404
from pages.models import Anime, Episodes
from django.http import Http404
from account.models import *
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import  force_bytes, force_str, force_text
# Create your views here.
def anime(request, slug):
    try:
        anime = get_object_or_404(Anime, name=force_text(urlsafe_base64_decode(slug)))
    except:
        raise Http404
    
    domain = get_current_site(request)
    class_fav = ''
    
    anime.url_anime = urlsafe_base64_encode(force_bytes(anime.pk))
    episodes = Episodes.objects.filter(name=anime).order_by('episode')
    class_done = ''
    class_want = '' 
    
    if request.user.is_authenticated:
        if UsersBack.objects.filter(user=request.user, animes_fav=anime):
            class_fav = 'favorite'
        if done_show.objects.filter(user=request.user, animes=anime).exists():
            class_done = 'favorite'
        if want_show.objects.filter(user=request.user, animes=anime).exists():
            class_want = 'favorite'

    
    for i in episodes:
        i.url_episode = urlsafe_base64_encode(force_bytes(i.pk))

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
        'class_want': class_want,
        'domain': domain,
    }

    return render(request, 'pages/anime-profile.html', x)

def watch(request, slug):
    try:
        episode = get_object_or_404(Episodes, pk=force_text(urlsafe_base64_decode(slug)))
    except:
        raise Http404
    
    domain = get_current_site(request)
    episodes = Episodes.objects.filter(name=episode.name).order_by('episode')

    #episode = Episodes.objects.get(name=anime, episode=str(eps_num))
    episode.title = episode.name.name.title()
    m = 'hide'
    n = 'hide'
    
    nex = episodes.filter(episode__gte=int(episode.episode))
    prvg = episodes.filter(episode__lte=int(episode.episode))

    
    if len(nex) > 1:
        n = nex[1]
        n.url_anime = urlsafe_base64_encode(force_bytes(n.id))
    
    if len(prvg) > 1:
        m = list(prvg)[-2]
        m.url_anime = urlsafe_base64_encode(force_bytes(m.id))


    for i in episodes:
        i.url_anime = urlsafe_base64_encode(force_bytes(i.id))
    
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