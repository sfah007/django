
from django.conf.urls import url
from django.core import paginator
from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from .models import *
from django.contrib.admin.models import *
from django.contrib import auth
from pages.models import *
from django.http import JsonResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.mail import *
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import  force_bytes, force_str, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
import re
from django.conf import settings
from .utils import generate_token
from django.contrib import admin
from animes import urls
from django.urls import path, include
from django.http import *
import secrets
import time
# Create your views here.

def ajax(request):
    
    #return render(request, 'pages/error500.html')
    return JsonResponse({'user': 'hamza'})

def send_message(user,request):
    domain = get_current_site(request)
    subject = 'Activate Your Account'
    token = secrets.token_hex(14).title()
    tk = Tokens(user=user, token=token, work='activate_account').save()
    context = {
        'user':user,
        'domain': domain,
        'uid': urlsafe_base64_encode(force_bytes(user.email)),
        'token': token,
    }

    body = render_to_string('account/activate.html', context)

    # Please use the link below to verify your account.

    # https://{domain}/account/activate-user/{context["uid"]}/{context["token"]}'''

    try:
        send_mail(
            subject,
            body,
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False
        )
    except:
        return 'not'
    #return render(request, 'pages/index.html')

def user_profile(request, username):
    domain = get_current_site(request)
    try:
        user = User.objects.get(username=username)
    except:
        raise Http404
    try:
        user_back = UsersBack.objects.get(user=user, information_public=True)
    except:
        raise Http404
    x = {
        'user': user_back,
        'domain': domain,
        'title_tag': username
    }

    return render(request, 'users/user-profile.html', x)

def account_animes(request, username, inf):
    domain = get_current_site(request)
    try:
        user = User.objects.get(username=username)
    except:
        raise Http404
    try:
        user_back = UsersBack.objects.get(user=user, information_public=True)
    except:
        raise Http404

    if inf == 'الأنميات-المفضلة' :
        paginator = Paginator(user_back.animes_fav.all(), 24)
        title = 'الأنميات المفضلة'

    elif inf == 'تم-مشاهدتها':
        paginator = Paginator(user_back.animes_done.all(), 24)
        title = 'أنميات تم مشاهدتها'

    elif inf == 'أرغب-بمشاهدتها':
        paginator = Paginator(user_back.animes_want.all(), 24)
        title = 'أنميات أرغب بمشاهدتها'

    else:
        raise Http404

    s = 1
    title = 'الأنميات المفضلة'
    anime_type = AnimeType.objects.all()
    anime_state = AnimeState.objects.all()
    anime_date = AnimeDate.objects.all()
    anime_class = AnimeClass.objects.all()

    if request.method == 'GET':
            if 'page' in request.GET:
                s = request.GET['page']

    

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
        anime.url_anime = urlsafe_base64_encode(force_bytes(anime.name))
        anime.title = anime.name.title()

    for i in anime_class:
        i.url_anime = i.name.replace(' ', '-')

    for i in anime_state:
        i.url_anime = i.name.replace(' ', '-')

    for i in anime_type:
        i.url_anime = i.name.replace(' ', '-')
    
    x = {
        'title': title,
        'page': page,
        'anime_type': anime_type,
        'anime_state': anime_state,
        'anime_date': anime_date,
        'anime_class': anime_class,
        'domain': domain,
        'title_tag': username
    }
    return render(request, 'pages/list-anime.html', x)


def reset_password(request):
    if request.user.is_authenticated:
        return redirect('index')
    messages = []
    error = None
    domain = get_current_site(request)
    if request.method == 'POST':
        if not ('email' in request.POST):
            error = 'بريدك الإلكتروني فارغ'
        else:
            email = request.POST['email']
            user = None
            try:
                user = User.objects.get(email=email)
            except:
                error = 'بريدك الإلكتروني غير صحيح'
            try:
                user = UsersBack.objects.get(user=user, is_active=True)
                user = user.user
            except:
                error = 'بريدك الإلكتروني غير مفعل'
                user = None 
            if user:
                
                try:
                    tk = Tokens.objects.get(user=user, work='reset_password').delete()
                except:
                    pass
                token = secrets.token_hex(14).title()
                token_db = Tokens(user=user, token=token, work='reset_password').save()
               
                subject = 'reset password'
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                
                body = f'''
                You're receiving this email because you requested a password reset for your user account at {domain}.

                Please use the link below to reset your Password

                http://{domain}/account/reset-password/{uid}/{token}/

                Your username, in case you’ve forgotten: {user.username}
                
                '''
               

                try:
                    send_mail(
                        subject,
                        body,
                        settings.EMAIL_HOST_USER,
                        [user.email],
                        fail_silently=False
                    )
                    messages.append('المرجو التحقق من بريدك الالكتروني')
                except:
                    error = 'خطأ'

    x = {
        'page': 'reset_password',
        'error': error,
        'title': 'تغيير كلمة السر',
        'messages': messages,
        'domain': domain
    }
    return render(request, 'account/login.html', x)

def reset_password_confirm(request, uidb64, token):
    if request.user.is_authenticated:
        raise Http404
    
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        
    except Exception as e :
        user=None
    
    try:
        tk = Tokens.objects.get(user=user, work='reset_password')
        
    except Exception as e :
        tk=None

    messages = []
    error = None
    if user and tk :
        if request.POST:
            if not('password1' in request.POST):
                error = 'الحقل الأول فارغ'
            elif not('password2' in request.POST):
                error = 'الحقل الثاني فارغ'
            else:
                password1 = request.POST['password1']
                password2 = request.POST['password2']

                if password1 != password2:
                    error = 'كلمة المرور غير متطابقة'
                elif password1.find(' ') != -1:
                    error = 'كلمة المرور يجب ألا يحتوي على مسافات'
                elif len(password1) <= 8:
                     error = 'كلمة المرور يجب أن تكون أكثر من 8 حروف'
                elif password1.isdigit():
                    error = 'كلمة المرور لا يجب أن تحتوي على أرقام فقط'
                else:
                    user.set_password(password1)
                    user.save()
                    k = tk.delete()

                    auth.login(request, user)
                    return redirect('index')
        x = {
            'title': 'تغيير كلمة السر',
            'title_tag': 'تغيير كلمة السر',
            'error': error,
            'domain': get_current_site(request),
        }
        return render(request, 'account/reset.html', x) 
    raise Http404


def register(request):
    if not request.user.is_authenticated:

        val_email = ''
        val_user = ''
        val_pass1 = ''
        val_pass2 = ''
        error = None
        if request.method == "POST":
            username = ''
            email = ''
            password1 = ''
            password2 = ''
            terms = ''
            if 'username' in request.POST:
                username = request.POST['username']

            if 'email' in request.POST:
                email = request.POST['email']

            if 'password1' in request.POST:
                password1 = request.POST['password1']

            if 'password2' in request.POST:
                password2 = request.POST['password2']
            if 'terms' in request.POST:
                terms = request.POST['terms']

            
            val_pass1 = password1
            val_pass2 = password2
            val_user = username
            val_email = email

            if terms != 'on':
                error = 'أنت غير موافق على الشروط'
            elif not (username and email and password1 and password2) :
                error = 'حقل فارغ'
            elif username.find(' ') != -1:
                error = 'سم المستخدم يجب ألا يحتوي على مسافات'
            elif User.objects.filter(username=username).exists():
                    error = 'اسم المستخدم موجود مسبقاً'
            elif User.objects.filter(email=email).exists():
                    error = 'هذا البريد الإلكتروني موجود مسبقا'
            elif email.find('@') < 6 or not re.fullmatch(r'\b[A-Za-z0-9]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', email):
                error = 'هناك خطأ في بريدك الإلكتروني'
            elif len(email) <= 15:
                error = 'البريد الالكتروني يجب أن يكون أكثر من 15 حرف'
            elif password1 != password2:
                error = 'كلمة المرور غير متطابقة'
            elif password1.find(' ') != -1:
                error = 'كلمة المرور يجب ألا يحتوي على مسافات'
            elif len(password1) <= 8:
                    error = 'كلمة المرور يجب أن تكون أكثر من 8 حروف'
            elif password1.isdigit():
                error = 'كلمة المرور لا يجب أن تحتوي على أرقام فقط'
            else:
                cr_user = User.objects.create_user(username=username, email=email,password=password1)
                if send_message(cr_user, request)  == 'not':
                    cr_user.delete()
                    error = 'بريدك الإلكتروني غير صحيح'
                else:
                    x = {
                        'message': 'تم إنشاء حسابك بنجاح. المرجو التحقق من بريدك الإلكتروني'
                    }

                    return render(request, 'account/register.html', x)
            



        x = {
            'error':error,
            'user_value': val_user,
            'email_value': val_email,
            'pass1_value': val_pass1,
            'pass2_value': val_pass2,
            'register': True,
            'domain': get_current_site(request),
        }

        return render(request, 'account/register.html', x)
    else:
        return redirect('index')

def account(request):
    if not(request.user.is_authenticated):
        return redirect('login')
    context = {
        'user': request.user.user,
        'page': 'account'
    }
    return render(request, 'users/user-profile.html', context)


def login(request):
    if not request.user.is_authenticated:
        error = None
        form = LoginForm()
        if request.method == "POST":
            if 'username' in request.POST and 'password' in request.POST:
                username = request.POST['username']
                password = request.POST['password']

                if username and password:
                    
                    user = auth.authenticate(username=username, password=password)


                    if UsersBack.objects.filter(user=user, is_active=False).exists():
                            error = 'المرجو تفعيل حسابك'
                    else:
                        if user is not None:

                            auth.login(request, user)
                            return redirect('account')
                        else:
                            error = 'اسم المستخدم او كلمة المرور غير صحيحة'
                else:
                    error = 'حقل فارغ'
            else:
                error = 'حقل فارغ'
        x = {
            'form': form,
            'error': error,
            'page': 'login',
            'domain': get_current_site(request),
            'title': 'تسجيل الدخول',
            'title_tag': 'سجل حسابك لمشاهدة احدث حلقات و أفلام الانمي مترجمة اون لاين ',
        }

        return render(request, 'account/login.html', x)
    else:
        return redirect('index')
def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)

    return redirect('index')

def animes_favorites_check(request, name):
    try:
        anime = get_object_or_404(Anime, pk=force_text(urlsafe_base64_decode(name)))
    except:
        raise Http404

    if request.user.is_authenticated and not request.user.is_anonymous :
        if request.is_ajax():
            url = urlsafe_base64_encode(force_bytes(anime.name))
            user_back = UsersBack.objects.get(user=request.user)
            if UsersBack.objects.filter(user=request.user, animes_fav=anime).exists():
                user_back.animes_fav.remove(anime)
                res = False
            else:
                user_back.animes_fav.add(anime)
                res = True

            return JsonResponse({'res': res})
        raise Http404
    else:
        return redirect('login')



def animes_favorites(request):
    if request.user.is_authenticated and not request.user.is_anonymous :
        title = 'الأنميات المفضلة'
        s = 1
        if request.method == 'GET':
            if 'page' in request.GET:
                s = request.GET['page']
        user_back = get_object_or_404(UsersBack, user=request.user)
        paginator = Paginator(user_back.animes_fav.all(), 24)


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
            i.title = i.name.title()
            i.url_anime = urlsafe_base64_encode(force_bytes(i.name))



        x = {
            'title': title,
            'page': page,
            'domain': get_current_site(request),
        }

        return render(request, 'account/animes-favorites.html', x)
    else:
        return redirect('login')


def done_show_check(request, name):
    try:
        anime = get_object_or_404(Anime, pk=force_text(urlsafe_base64_decode(name)))
    except:
        raise Http404

    if request.user.is_authenticated and not request.user.is_anonymous :
        if request.is_ajax():
            url = urlsafe_base64_encode(force_bytes(anime.name))
            done = UsersBack.objects.get(user=request.user)
            if UsersBack.objects.filter(user=request.user, animes_done=anime).exists():
                done.animes_done.remove(anime)
                res = False
            else:
                done.animes_done.add(anime)
                res = True

            return JsonResponse({'res': res})
        raise Http404
    else:
        return redirect('login')


def done_show_views(request):
    if request.user.is_authenticated and not request.user.is_anonymous :
        title = 'انميات تم مشاهدتها'
        s = 1
        if request.method == 'GET':
            if 'page' in request.GET:
                s = request.GET['page']
        user_back = get_object_or_404(UsersBack, user=request.user)
        paginator = Paginator(user_back.animes_done.all(), 24)


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
            i.title = i.name.title()
            i.url_anime = urlsafe_base64_encode(force_bytes(i.name))



        x = {
            'title': title,
            'page': page,
            'domain': get_current_site(request),
        }

        return render(request, 'account/animes-favorites.html', x)
    else:
        return redirect('login')

def want_show_check(request, name):
    try:
        name = force_text(urlsafe_base64_decode(name))
        anime = get_object_or_404(Anime, pk=name)
    except:
        raise Http404

    if request.user.is_authenticated and not request.user.is_anonymous :
        if request.is_ajax():
            url = urlsafe_base64_encode(force_bytes(anime.name))
            want = UsersBack.objects.get(user=request.user)
            if UsersBack.objects.filter(user=request.user, animes_want=anime).exists():
                want.animes_want.remove(anime)
                res = False
            else:
                want.animes_want.add(anime)
                res = True

            return JsonResponse({'res': res})
        raise Http404
    else:
        return redirect('login')

def want_show_views(request):
    if request.user.is_authenticated and not request.user.is_anonymous :
        title = 'أرغب بمشاهدته'
        s = 1
        if request.method == 'GET':
            if 'page' in request.GET:
                s = request.GET['page']
        user_back = get_object_or_404(UsersBack, user=request.user)
        paginator = Paginator(user_back.animes_want.all(), 24)

        
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
            i.title = i.name.title()
            i.url_anime = urlsafe_base64_encode(force_bytes(i.name))

        
        x = {
            'title': title,
            'page': page,
            'domain': get_current_site(request),
        }

        return render(request, 'account/animes-favorites.html', x)
    else:
        return redirect('login')

def activate(request, uidb64, token):
    if request.user.is_authenticated:
        raise Http404

    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(email=uid)
    except Exception as e :
        user=None

    try:
        tk = Tokens.objects.get(user=user, work='activate_account')
    except:
        tk = None

    if user and tk:
        user_back = UsersBack.objects.get(user=user)
        user_back.is_active = True
        user_back.save()
        k = tk.delete()
        auth.login(request, user)
        return redirect('index')
    raise Http404

