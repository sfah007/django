from django.urls import path, re_path
from . import views

urlpatterns = [
    re_path(r'^(?P<slug>[-0-9a-zA-Z\.]+)/$', views.anime, name='anime'),
    re_path(r'^(?P<slug>[-0-9a-zA-Z\.]+)/(?P<eps_num>[-0-9a-zA-Z\.]+)/$', views.watch, name='watch'),
    
]