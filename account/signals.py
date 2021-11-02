from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from django.contrib.auth.models import User
from .models import *

from django.core.mail import send_mail
from django.conf import settings


def createProfile(sender, instance, created, **kwargs):
    if created == True:
        
        user = instance
        profile = UsersBack(
            user=user
        )
        profile.save()

        subject = 'Welcome to hamzaanimes'
        message = 'We are glad you are here!'
       
        try:
            send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False,
            )
        except:
            pass
        
def UpdateProfile(sender, instance, created, **kwargs):
    if created == False:

        profile = instance
        print(profile.username)
        user = User.objects.get(username=profile.user.username)
        print(user.username)
        user.username = profile.username
        user.email = profile.email
        user.save()

post_save.connect(createProfile, sender=User)
#post_save.connect(UpdateProfile, sender=UsersBack)