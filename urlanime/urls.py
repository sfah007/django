from django.urls import path, re_path
from . import views

urlpatterns = [
    path('<str:slug>/', views.anime, name='anime'),
    path('episode/<str:slug>/', views.watch, name='watch'),
    
]