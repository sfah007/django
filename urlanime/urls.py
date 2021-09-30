from django.urls import path, re_path
from . import views

urlpatterns = [
    path('<str:slug>/', views.anime, name='anime'),
    path('<str:slug>/<int:eps_num>/', views.watch, name='watch'),
    
]