from django.db import models
from django.contrib.auth.models import User
from pages.models import *
import uuid
from django.utils import timezone
from PIL import Image
from  django.conf import settings
import os
# Create your models here.
class UsersBack(models.Model):
    choices = (
        ('prive', 'prive'),
        ('public', 'public')
    )

    user = models.OneToOneField(User,  related_name='user',on_delete=models.CASCADE)

    bio = models.TextField(blank=True, null=True)

    profile_image = models.ImageField(
        null=True, blank=True, upload_to='profiles/', default="profiles/user-default.png")

    animes_fav = models.ManyToManyField(Anime, related_name='fav', blank=True)

    animes_done = models.ManyToManyField(Anime, related_name='done', blank=True) 

    animes_want = models.ManyToManyField(Anime, related_name='want', blank=True) 

    following = models.ManyToManyField(User, related_name='following',blank=True) 

    social_twitter = models.CharField(max_length=200, blank=True, null=True)

    social_instagram = models.CharField(max_length=200, blank=True, null=True)

    social_github = models.CharField(max_length=200, blank=True, null=True)

    social_website = models.URLField(max_length=200, blank=True, null=True)
    
    created = models.DateTimeField(default=timezone.now)

    information_public = models.BooleanField(default=True)

    notification = models.BooleanField(default=True)

    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
    
    def save(self):
        super().save()
        if self.profile_image.width > 300 and self.profile_image.height > 300:
            size = (300, 300)
            img = Image.open(self.profile_image.path)
            img.thumbnail(size)
            img.save(self.profile_image.path)


    @property
    def imageURL(self):
        try:
            url = self.profile_image.url
        except:
            url = ''
        return url

class Tokens(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=200)
    work = models.CharField(max_length=200)
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.token

class Domain(models.Model):
    domain = models.CharField(max_length=400)
