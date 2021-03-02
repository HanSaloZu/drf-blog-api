# Generated by Django 3.1.7 on 2021-02-27 21:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_auto_20210228_0003'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='contacts',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='photos',
        ),
        migrations.AddField(
            model_name='contacts',
            name='profile',
            field=models.OneToOneField(default='123', on_delete=django.db.models.deletion.CASCADE, to='profiles.profile'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='photos',
            name='profile',
            field=models.OneToOneField(default='123', on_delete=django.db.models.deletion.CASCADE, to='profiles.profile'),
            preserve_default=False,
        ),
    ]