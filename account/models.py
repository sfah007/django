from django.db import models
from django.contrib.auth.models import User
from pages.models import *
import uuid
# Create your models here.
class UsersBack(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    animes_fav = models.ManyToManyField(Anime)
    username = models.CharField(max_length=30)
    email = models.EmailField()
    password = models.CharField(max_length=30)

    def __str__(self):
        return self.username