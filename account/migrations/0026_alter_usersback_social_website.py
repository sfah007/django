# Generated by Django 3.2.8 on 2021-10-31 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0025_auto_20211031_0632'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersback',
            name='social_website',
            field=models.URLField(blank=True, null=True),
        ),
    ]
