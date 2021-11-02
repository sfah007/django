# Generated by Django 3.2.4 on 2021-10-28 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0005_auto_20211026_0640'),
        ('account', '0010_auto_20211028_0524'),
    ]

    operations = [
        migrations.AddField(
            model_name='usersback',
            name='animes_done',
            field=models.ManyToManyField(blank=True, related_name='done', to='pages.Anime'),
        ),
        migrations.AddField(
            model_name='usersback',
            name='animes_want',
            field=models.ManyToManyField(blank=True, related_name='want', to='pages.Anime'),
        ),
        migrations.AlterField(
            model_name='usersback',
            name='animes_fav',
            field=models.ManyToManyField(blank=True, related_name='fav', to='pages.Anime'),
        ),
    ]
