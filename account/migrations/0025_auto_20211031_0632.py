# Generated by Django 3.2.8 on 2021-10-31 13:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0024_alter_usersback_profile_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usersback',
            name='email',
        ),
        migrations.RemoveField(
            model_name='usersback',
            name='username',
        ),
    ]
