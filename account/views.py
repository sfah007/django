from django.shortcuts import render, redirect
from .forms import *
from .models import *
from django.contrib.admin.models import * 
from django.contrib import auth
from pages.models import *
from django.http import JsonResponse
import re
# Create your views here.

def register(request):
    if not request.user.is_authenticated:
        val_email = ''
        val_user = ''
        val_pass1 = ''
        val_pass2 = ''
        error = None
        if request.method == "POST":
            username = request.POST['username']
            email = request.POST['email']
            password1 = request.POST['password1']
            password2 = request.POST['password2']

            val_user = username
            val_email = email
            val_pass1 = password1
            val_pass2 = password2
            
            if username and email and password1 and password2 :
                if User.objects.filter(username=username).exists():
                    error = 'اسم المستخدم موجود مسبقاً'
                else:
                    if User.objects.filter(email=email).exists():
                        error = 'هذا البريد الإلكتروني موجود مسبقا'
                    else:
                        if email.endswith('@gmail.com'):
                            if password1 != password2:
                                error = 'كلمة المرور غير متطابقة'
                            else:
                                cr_user = User.objects.create_user(username=username, email=email,password=password1)
                                cr_user.save()
                                
                                user_back = UsersBack(user=cr_user, username=username, email=email, password=password1)
                                user_back.save()
                            
                                user = auth.authenticate(username=username, password=password1)
                                if user is not None:
                                    auth.login(request, user)
                                return redirect('index')
                        else:
                            error = 'خطأ في البريد الالكتروني'
        

        x = {
            'error':error,
            'user_value': val_user,
            'email_value': val_email,
            'pass1_value': val_pass1,
            'pass2_value': val_pass2,
        }

        return render(request, 'account/register.html', x)
    else:
        return redirect('index')

def login(request):
    if not request.user.is_authenticated:
        error = None
        form = LoginForm()
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']

            user = auth.authenticate(username=username, password=password)
            if  user is not None:
                auth.login(request, user)
                return redirect('index')
            else:
                error = 'اسم المستخدم او كلمة المرور غير صحيحة'


        x = {
            'form': form,
            'error': error,
        }

        return render(request, 'account/login.html', x)
    else:
        return redirect('index')
def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
    
    return redirect('index')

def animes_favorites(request, name):
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
