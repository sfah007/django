from django.db import models
from django.db.models.base import Model
from datetime import datetime
from django.utils import timezone
import pytz

from django.core.validators import FileExtensionValidator


# Create your models here.

    

class AnimeType(models.Model):
    name = models.CharField(unique=True, max_length=50)
    publish_date = models.DateTimeField( default=timezone.now)

    class Meta:
        ordering = ['-publish_date']

    def __str__(self):
        return self.name


class AnimeState(models.Model):
    name = models.CharField(unique=True, max_length=50)
    publish_date = models.DateTimeField( default=timezone.now )

  
    def __str__(self):
        return self.name


class AnimeClass(models.Model):
    name = models.CharField(unique=True, max_length=50)
    publish_date = models.DateTimeField( default=timezone.now )

    class Meta:
        ordering = ['publish_date']

    def __str__(self):
        return self.name
    
class AnimeDate(models.Model):
    name = models.CharField(unique=True, max_length=50)
    publish_date = models.DateTimeField( default=timezone.now )

    class Meta:
        ordering = ['publish_date']

    def __str__(self):
        return self.name

class AnimeDays(models.Model):
    name = models.CharField(unique=True ,max_length=50)
    publish_date = models.DateTimeField( default=timezone.now )

    class Meta:
        ordering = ['publish_date']

    def __str__(self):
        return self.name

class Anime(models.Model):
    name = models.CharField(unique=True, max_length=50)

    story = models.TextField( default='')

    image_anime = models.ImageField( upload_to='photos/anime', default='')

    anime_type = models.ForeignKey(AnimeType, on_delete=models.CASCADE)

    anime_state = models.ForeignKey(AnimeState, on_delete=models.CASCADE)

    anime_date = models.ForeignKey(AnimeDate, on_delete=models.CASCADE)

    anime_days = models.ForeignKey(AnimeDays, on_delete=models.CASCADE)

    anime_class = models.ManyToManyField(AnimeClass)

    number_episodes = models.CharField( max_length=50)

    episode_date = models.CharField( max_length=50)

    publish_date = models.DateTimeField( default=timezone.now )

    class Meta:
        ordering = ['-publish_date']

    def __str__(self):
        return self.name

class Episodes(models.Model):
    choices = (
        ('video', 'video'),
        ('url', 'url')
    )

    choices_html = (
        ('video', 'video'),
        ('iframe', 'iframe')
    )

    name = models.ForeignKey(Anime, on_delete=models.CASCADE)
    episode = models.IntegerField()
    type_episode = models.CharField(blank=True, choices=choices, max_length=50) 
    type_html = models.CharField(blank=True, choices=choices_html, max_length=50) 
    url = models.URLField( max_length=200, default='', blank=True)
    video = models.FileField(blank=True, upload_to='video/anime/%Y/%m/%d', max_length=500, validators=[FileExtensionValidator(allowed_extensions=['MOV','avi','mp4','webm','mkv'])])
    publish_date = models.DateTimeField( default=timezone.now )

    class Meta:
        ordering = ['-publish_date']

    def __str__(self):
        return f'{self.name} {self.episode}'



