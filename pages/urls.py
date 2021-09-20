from django.urls import path, re_path
from . import views
from django.views.static import serve 
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}), 
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}), 
    path('', views.index, name='index'),
    path('قائمة-الأنمي/', views.list_anime, name='list_anime'),
    re_path(r'^(?P<name>[-a-zA-Z0-9 ]+)/(?P<slug>[-\u0621-\u064A\u0660-\u0669 0-9 ]+)/$', views.ht, name='ht'),
    
    path('episode/', views.episode, name='episode'),
    path('search/', views.search, name='search'),
    path('مواعيد-عرض-حلقات-الانمي/', views.days_anime, name='days_anime')
]