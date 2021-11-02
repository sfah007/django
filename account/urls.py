from os import terminal_size
from django.urls import path, re_path
from django.conf.urls import url
from . import views
from django.contrib.auth.views import *

urlpatterns = [
    path('register/', views.register, name='register'),
    path('', views.account, name='account'),
    path('login/', views.login, name='login'),
    path('reset-password/', views.reset_password, name='reset_password'),
    path('reset-password/<uidb64>/<token>/', views.reset_password_confirm, name="password_reset_confirm"),
    path('user/<str:username>/', views.user_profile, name='user_profile'),
    path('user/<str:username>/<str:inf>/', views.account_animes, name='account_animes'),
    path('logout/', views.logout, name='logout'),
    path('animes-favorite/<str:name>/', views.animes_favorites_check, name='animes-favorite_check'),
    path('animes-favorite/', views.animes_favorites, name='animes-favorite'),
    path('تم-مشاهدتها/<str:name>/', views.done_show_check, name='done_show_add'),
    path('تم-مشاهدتها/', views.done_show_views, name='done_show'),
    path('أرغب-بمشاهدتها/<str:name>/', views.want_show_check, name='want_show_add'),
    path('أرغب-بمشاهدتها/', views.want_show_views, name='want_show'),
    path('activate-user/<uidb64>/<token>/', views.activate, name='activate'),
]