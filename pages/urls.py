from django.urls import path, re_path
from . import views
from django.views.static import serve 
from django.conf.urls.static import static
from django.conf import settings
from account.views import login 

urlpatterns = [
    re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}), 
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}), 
    path('', views.index, name='index'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('admin/login/', views.page_reset, name='admin-login'),
    path('قائمة-الأنمي/', views.list_anime, name='list_anime'),
    path('categorie/<str:name>/<str:slug>/', views.ht, name='ht'),
    path('episode/', views.episode, name='episode'),
    path('search/', views.search, name='search'),
    path('مواعيد-عرض-حلقات-الانمي/', views.days_anime, name='days_anime')
]