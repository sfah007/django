from os import terminal_size
from django.urls import path, re_path
from django.conf.urls import url
from . import views
from django.contrib.auth.views import *

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('animes-favorite/<str:name>', views.animes_favorites, name='animes-favorite'),
]