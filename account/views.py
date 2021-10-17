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
# Create your views here.

def send_message(user,request):
    domain = get_current_site(request)
    subject = 'Activate Your Account'
    context = {
        'user':user,
        'domain': domain,
        'uid': urlsafe_base64_encode(force_bytes(user.email)),
        'token': generate_token.make_token(user)
    }

    body = render_to_string('account/activate.html', context)
    
    # Please use the link below to verify your account.
    
    # https://{domain}/account/activate-user/{context["uid"]}/{context["token"]}'''
    
    send_mail(
        subject,
        body,
        settings.EMAIL_HOST_USER,
        [user.email],
        fail_silently=False
    )

    #return render(request, 'pages/index.html')


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
            if 'username' in request.POST:
                username = request.POST['username']

            if 'email' in request.POST:
                email = request.POST['email']

            if 'password1' in request.POST:
                password1 = request.POST['password1']

            if 'password2' in request.POST:
                password2 = request.POST['password2']
            

            val_pass1 = password1
            val_pass2 = password2
            val_user = username
            val_email = email

            if username and email and password1 and password2  :
                if User.objects.filter(username=username).exists():
                    error = 'اسم المستخدم موجود مسبقاً'
                else:
                    if User.objects.filter(email=email).exists():
                        error = 'هذا البريد الإلكتروني موجود مسبقا'
                    else:
                        if password1 != password2:
                            error = 'كلمة المرور غير متطابقة'
                        else:
                            if email.find('@') < 6 or len(email) < 14:
                                error = 'هناك خطأ في بريدك الإلكتروني'
                            else:
                                if email.find('@gmail.com') == -1:
                                    error = 'نقبل فقط البريد الإلكتروني الخاص ب gmail'
                                else:
                                    if len(password1) < 8 or len(password2) < 8:
                                        error = 'كلمة المرور أقل من 8 أحرف'
                                    else:
                                        cr_user = User.objects.create_user(username=username, email=email,password=password1)
                                        user_back = UsersBack(user=cr_user, is_active=False)
                                        user_back.save()  
                            
                                        send_message(cr_user, request) 
                                        x = {
                                            'message': 'تم إنشاء حسابك بنجاح. المرجو التحقق من بريدك الإلكتروني'
                                        }
                                        
                                        return render(request, 'account/register.html', x)
            else:
                error = 'حقل فارغ' 
                        
        

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
                            return redirect('index')
                        else:
                            error = 'اسم المستخدم او كلمة المرور غير صحيحة'
                else:
                    error = 'حقل فارغ' 
            else:
                error = 'حقل فارغ'
        x = {
            'form': form,
            'error': error,
            'domain': get_current_site(request),
        }

        return render(request, 'account/login.html', x)
    else:
        return redirect('index')
def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
    
    return redirect('index')

def animes_favorites_check(request, name):
    anime = Anime.objects.get(name=name.replace('-', ' '))
    if request.user.is_authenticated and not request.user.is_anonymous :
        user_back = UsersBack.objects.get(user=request.user)
        if UsersBack.objects.filter(user=request.user, animes_fav=anime).exists():
            user_back.animes_fav.remove(anime)
        else:
            user_back.animes_fav.add(anime)
        
        return redirect(f'/anime/{name}/')
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
            i.url_anime = i.name.replace(' ', '-')
            i.url_date = i.anime_date.name.replace(' ', '-')
            

        x = {
            'title': title,
            'page': page,
            'domain': get_current_site(request),
        }    
        
        return render(request, 'account/animes-favorites.html', x)
    else:
        return redirect('login')


def activate(request, uidb64, token):
    
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(email=uid)
    except Exception as e :
        user=None

    if user and generate_token.check_token(user, token):
        user_back = UsersBack.objects.get(user=user)
        user_back.is_active = True
        user_back.save()

        print(user)
        auth.login(request, user)
        return redirect('index')