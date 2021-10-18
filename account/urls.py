from os import terminal_size
from django.urls import path, re_path
from django.conf.urls import url
from . import views
from django.contrib.auth.views import *

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('animes-favorite/add/<str:name>/', views.animes_favorites_check, name='animes-favorite_check'),
    path('animes-favorite/', views.animes_favorites, name='animes-favorite'),
    path('تم-مشاهدتها/add/<str:name>/', views.done_show_check, name='done_show_add'),
    path('تم-مشاهدتها/', views.done_show_views, name='done_show'),
    path('activate-user/<uidb64>/<token>/', views.activate, name='activate'),
]