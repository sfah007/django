# Generated by Django 3.2.4 on 2021-10-28 12:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0011_auto_20211028_0526'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='want_show',
            name='animes',
        ),
        migrations.RemoveField(
            model_name='want_show',
            name='user',
        ),
        migrations.DeleteModel(
            name='done_show',
        ),
        migrations.DeleteModel(
            name='want_show',
        ),
    ]
