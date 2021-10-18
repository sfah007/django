from django.db import models
from django.contrib.auth.models import User
from pages.models import *
import uuid
# Create your models here.
class UsersBack(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    animes_fav = models.ManyToManyField(Anime, blank=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

class done_show(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    animes = models.ManyToManyField(Anime, blank=True) 

    def __str__(self):
        return self.user.username