from django.db.models.signals import *
from django.conf import Settings, settings
from .models import *
from django.core.mail import *
from django.contrib.auth.models import User
from account.models import *
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import  force_bytes, force_str, force_text

#from django.contrib.sites.shortcuts import get_current_site


def CreateEpisode(sender, instance, created, **kwargs):
    
    if created :
        episode = instance
        users = UsersBack.objects.filter(animes_fav=episode.name, is_active=True, notification=True)
        name = episode.name.name.title()
        subject = f'حلقة جديدة من أنمك المفضل {name}'
        eps_url = urlsafe_base64_encode(force_bytes(episode.pk))
        domain = Domain.objects.all()[0].domain
        for user in users:
            body = f'''مرحبا {user.user.username} لقد نزلت الحلقة {episode.episode} من أنمك المفضل {name} على موقعنا
            
            http://{domain}/anime/episode/{eps_url}/'''
            try:
                send_mail(
                    subject,
                    body,
                    settings.EMAIL_HOST_USER,
                    [user.user.email],
                    fail_silently=False
                )
            except:
                print('Failed')



post_save.connect(CreateEpisode, sender=Episodes)