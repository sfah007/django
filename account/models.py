from django.db import models
from django.contrib.auth.models import User
from pages.models import *
import uuid
# Create your models here.
class UsersBack(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    animes_fav = models.ManyToManyField(Anime)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username