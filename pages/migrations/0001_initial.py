# Generated by Django 3.2.4 on 2021-10-15 07:19

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Anime',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('story', models.TextField(default='')),
                ('image_anime', models.ImageField(default='', upload_to='photos/anime')),
                ('number_episodes', models.CharField(max_length=50)),
                ('episode_date', models.CharField(max_length=50)),
                ('publish_date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'ordering': ['-publish_date'],
            },
        ),
        migrations.CreateModel(
            name='AnimeClass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('publish_date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'ordering': ['publish_date'],
            },
        ),
        migrations.CreateModel(
            name='AnimeDate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('publish_date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'ordering': ['publish_date'],
            },
        ),
        migrations.CreateModel(
            name='AnimeDays',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('publish_date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'ordering': ['publish_date'],
            },
        ),
        migrations.CreateModel(
            name='AnimeState',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('publish_date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='AnimeType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('publish_date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'ordering': ['-publish_date'],
            },
        ),
        migrations.CreateModel(
            name='Episodes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('episode', models.IntegerField()),
                ('type_episode', models.CharField(blank=True, choices=[('video', 'video'), ('url', 'url')], max_length=50)),
                ('type_html', models.CharField(blank=True, choices=[('video', 'video'), ('iframe', 'iframe')], max_length=50)),
                ('url', models.URLField(blank=True, default='')),
                ('video', models.FileField(blank=True, max_length=500, upload_to='video/anime/%Y/%m/%d', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['MOV', 'avi', 'mp4', 'webm', 'mkv'])])),
                ('publish_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pages.anime')),
            ],
            options={
                'ordering': ['-publish_date'],
            },
        ),
        migrations.AddField(
            model_name='anime',
            name='anime_class',
            field=models.ManyToManyField(to='pages.AnimeClass'),
        ),
        migrations.AddField(
            model_name='anime',
            name='anime_date',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pages.animedate'),
        ),
        migrations.AddField(
            model_name='anime',
            name='anime_days',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pages.animedays'),
        ),
        migrations.AddField(
            model_name='anime',
            name='anime_state',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pages.animestate'),
        ),
        migrations.AddField(
            model_name='anime',
            name='anime_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pages.animetype'),
        ),
    ]
