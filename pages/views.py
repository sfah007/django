from django.shortcuts import redirect, render, get_object_or_404
from .models import AnimeDays, AnimeState, AnimeClass, AnimeDate, AnimeType, Anime, Episodes
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
# Create your views here.
from django.contrib.sites.shortcuts import get_current_site


def index(request):
    episodes = Episodes.objects.all()[:24]
    animes = Anime.objects.all()[:24]

    for anime in animes:
        anime.url_anime = anime.name.replace(' ','-')
        anime.title = anime.name.title()
        anime.url_date = anime.anime_date.name.replace(' ', '-')

    for episode in episodes:
        episode.name.number_episodes = episode.name.name.replace(' ', '-')
        episode.name.episode_date = episode.name.name.title()



    x = {
        'episodes': episodes,
        'animes_search': animes,
        'domain': get_current_site(request),
    }

    return render(request, 'pages/index.html', x)



# list-anime
def list_anime(request):

    s = 1
    title = 'الأنميات'
    anime_type = AnimeType.objects.all()
    anime_state = AnimeState.objects.all()
    anime_date = AnimeDate.objects.all()
    anime_class = AnimeClass.objects.all()
    animes = Anime.objects.all()

    
    res = {}
    out = list(anime_date)
    ln = len(out)
    for i in range(ln):
        t = []
        for x in out[ln-1-i].name:
            if x.isdigit():
                t.append(x)
        t = int(''.join(t))
        if t in res:
            res[t].append(out[ln-1-i])
        else:
            res[t] = [out[ln-1-i]]
    
    anime_date = []
    num = []
    for i in res:
        num.append(i)
    
    num = sorted(num)
    for i in num:
        ln = len(res[i])
        
        for x in range(ln):
            anime_date.append(res[i][ln-1-x])
        


    if request.method == 'GET':
        if 'page' in request.GET:
            s = request.GET['page']
        if 's' in request.GET:
            sr = request.GET['s']
            title = f'نتائج البحث عن [ {sr} ]'
            animes = animes.filter(name__contains=sr)
        

    paginator = Paginator(animes, 24)

    try:
        page = paginator.page(s)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)  

    if page.number <= 1:
        page.range = range(page.number, paginator.num_pages+1)[:3]
    elif page.number == 2:
        page.range = range(page.number-1, paginator.num_pages+1)[:4]
    else:
        page.range = range(page.number-2, paginator.num_pages+1)[:5]



    for anime in page:
        anime.url_anime = anime.name.replace(' ','-')
        anime.title = anime.name.title()
        anime.url_date = anime.anime_date.name.replace(' ', '-')

    for i in anime_class:
        i.url_anime = i.name.replace(' ', '-')

    for i in anime_state:
        i.url_anime = i.name.replace(' ', '-')

    for i in anime_type:
        i.url_anime = i.name.replace(' ', '-')

    for i in anime_date:
        i.url_anime = i.name.replace(' ', '-')

    x = {
        'title': title,
        'anime_type': anime_type,
        'anime_state': anime_state,
        'anime_date': anime_date,
        'anime_class': anime_class,
        'page': page,
        'urlpath': f'قائمة افلام وانميات  مترجمة اون لاين',
    }


    return render(request, 'pages/list-anime.html', x)

# anime-genre ... => ht
def ht(request, name, slug):
    if name == 'anime-genre' or name == 'anime-state' or name == 'anime-type' or name == 'anime-season':
        s = 1
        anime_type = AnimeType.objects.all()
        anime_state = AnimeState.objects.all()
        anime_date = AnimeDate.objects.all()
        anime_class = AnimeClass.objects.all()
        animes = Anime.objects.all()

        res = {}
        out = list(anime_date)
        ln = len(out)
        for i in range(ln):
            t = []
            for x in out[ln-1-i].name:
                if x.isdigit():
                    t.append(x)
            t = int(''.join(t))
            if t in res:
                res[t].append(out[ln-1-i])
            else:
                res[t] = [out[ln-1-i]]
        
        anime_date = []
        num = []
        for i in res:
            num.append(i)
        
        num = sorted(num)
        for i in num:
            ln = len(res[i])
            
            for x in range(ln):
                anime_date.append(res[i][ln-1-x])
        slug_rep = slug.replace('-', ' ')
        if name == 'anime-state':
            cls = get_object_or_404(AnimeState, name=slug_rep)
            urlpath = f'{slug_rep}'
            animes = animes.filter(anime_state=cls)

            title = f'حالة الأنمي [ {cls.name} ]'
            
        
        elif name == 'anime-genre':
            cls = get_object_or_404(AnimeClass, name=slug_rep)
            urlpath = f'{slug_rep}'
            animes = animes.filter(anime_class=cls)

            title = f'تصنيف الأنمي [ {cls.name} ]'

        elif name == 'anime-type':
            cls = get_object_or_404(AnimeType, name=slug_rep)
            urlpath = f'{slug_rep}'
            animes = animes.filter(anime_type=cls)
            title = f'نوع الأنمي [ {cls.name} ]'

        elif name == 'anime-season':
            cls = get_object_or_404(AnimeDate, name=slug_rep)
            urlpath = f'موسم {slug_rep}'
            animes = animes.filter(anime_date=cls)

            title = f'الموسم [ {cls.name} ]'
            
        if request.method == 'GET':
            if 'page' in request.GET:
                s = request.GET['page']

        paginator = Paginator(animes, 24)

        try:
            page = paginator.page(s)
        except PageNotAnInteger:
            page = paginator.page(1)
        except EmptyPage:
            page = paginator.page(paginator.num_pages)  

        if page.number <= 1:
            page.range = range(page.number, paginator.num_pages+1)[:3]
        elif page.number == 2:
            page.range = range(page.number-1, paginator.num_pages+1)[:4]
        else:
            page.range = range(page.number-2, paginator.num_pages+1)[:5]
            
  

        for anime in page:
            anime.url_anime = anime.name.replace(' ','-')
            anime.title = anime.name.title()
            anime.url_date = anime.anime_date.name.replace(' ', '-')
        

        for i in anime_class:
            i.url_anime = i.name.replace(' ', '-')

        for i in anime_state:
            i.url_anime = i.name.replace(' ', '-')

        for i in anime_type:
            i.url_anime = i.name.replace(' ', '-')

        for i in anime_date:
            i.url_anime = i.name.replace(' ', '-')

        
        x = {
            'title': title,
            'anime_type': anime_type,
            'anime_state': anime_state,
            'anime_date': anime_date,
            'anime_class': anime_class,
            'page': page,
            'urlpath': f'قائمة افلام وانميات {urlpath} مترجمة اون لاين',
            'domain': get_current_site(request)

        }

        
        


        return render(request, 'pages/list-anime.html', x)
    else:
        return render(request, 'pages/error404.html')
    
    

# episode   
def episode(request):
    s = 1
    title = 'حلقات الأنمي'
    episode = Episodes.objects.all()


    if request.method == 'GET':
        if 'page' in request.GET:
            s = request.GET['page']

    paginator = Paginator(episode, 24)

    try:
        page = paginator.page(s)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)  

    if page.number <= 1:
        page.range = range(page.number, paginator.num_pages+1)[:3]
    elif page.number == 2:
        page.range = range(page.number-1, paginator.num_pages+1)[:4]
    else:
        page.range = range(page.number-2, paginator.num_pages+1)[:5]    


    for i in page:
        i.name.episode_date = i.name.name.title()
        i.name.number_episodes = i.name.name.replace(' ', '-')

    x = {
        'page': page,
        'ul_hide' : 'hide',
        'title': title,
    }


    return render(request, 'pages/episode.html', x)


# search

def search(request):
    s = 1
    title = 'نتائج البحث عن [  ]'
    anime_type = AnimeType.objects.all()
    anime_state = AnimeState.objects.all()
    anime_date = AnimeDate.objects.all()
    anime_class = AnimeClass.objects.all()
    animes = Anime.objects.all()
    search = 'hide'
    sr = ''

    res = {}
    out = list(anime_date)
    ln = len(out)
    for i in range(ln):
        t = []
        for x in out[ln-1-i].name:
            if x.isdigit():
                t.append(x)
        t = int(''.join(t))
        if t in res:
            res[t].append(out[ln-1-i])
        else:
            res[t] = [out[ln-1-i]]
    
    anime_date = []
    num = []
    for i in res:
        num.append(i)
    
    num = sorted(num)
    for i in num:
        ln = len(res[i])
        
        for x in range(ln):
            anime_date.append(res[i][ln-1-x])

    if request.method == 'GET':
        if 'page' in request.GET:
            s = request.GET['page']
        if 's' in request.GET:
            sr = request.GET['s']
            search = 'show'
            title = f'نتائج البحث عن [ {sr} ]'
            animes = animes.filter(name__icontains=sr)
            #sr = sr.replace(' ', '+')
            
    paginator = Paginator(animes, 24)

    try:
        page = paginator.page(s)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)  

    if page.number <= 1:
        page.range = range(page.number, paginator.num_pages+1)[:3]
    elif page.number == 2:
        page.range = range(page.number-1, paginator.num_pages+1)[:4]
    else:
        page.range = range(page.number-2, paginator.num_pages+1)[:5]


    for anime in page:
        anime.url_anime = anime.name.replace(' ','-')
        anime.title = anime.name.title()
        anime.url_date = anime.anime_date.name.replace(' ', '-')

    for i in anime_class:
        i.url_anime = i.name.replace(' ', '-')

    for i in anime_state:
        i.url_anime = i.name.replace(' ', '-')

    for i in anime_type:
        i.url_anime = i.name.replace(' ', '-')

    for i in anime_date:
        i.url_anime = i.name.replace(' ', '-')

    x = {
        'title': title,
        'anime_type': anime_type,
        'anime_state': anime_state,
        'anime_date': anime_date,
        'anime_class': anime_class,
        'page': page,
        'search': search,
        'search_text': sr.replace(' ','+'),
        'domain': get_current_site(request),
        'urlpath': f'نتائج البحث عن {sr}',
    }


    return render(request, 'pages/list-anime.html', x)

def days_anime(request):
    days = AnimeDays.objects.all()
    state = AnimeState.objects.get(name='مستمر')

    for i in days:
        
        i.animes = Anime.objects.filter(anime_days=i, anime_state=state)
        for x in i.animes:
            x.title = x.name.title()
            x.url = x.name.replace(' ', '-')
            x.url_date = x.anime_date.name.replace(' ', '-')


    x = {
        'days': days,
        'domain': get_current_site(request),
    }

    return render(request, 'pages/days_anime.html', x)

def page_reset(request):
    return redirect('index')