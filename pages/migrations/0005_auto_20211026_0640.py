# Generated by Django 3.2.4 on 2021-10-26 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0004_remove_anime_episode_date'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='animedate',
            options={'ordering': ['name']},
        ),
        migrations.AlterField(
            model_name='animedate',
            name='name',
            field=models.IntegerField(unique=True),
        ),
    ]
