# Generated by Django 3.1.7 on 2021-02-27 21:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_auto_20210227_2329'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contacts',
            options={'verbose_name': 'user contacts', 'verbose_name_plural': 'users contacts'},
        ),
        migrations.AlterModelOptions(
            name='photos',
            options={'verbose_name': 'profile photos', 'verbose_name_plural': 'profiles photos'},
        ),
    ]