# Generated by Django 3.2.3 on 2021-07-07 19:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('profiles', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='users.user')),
                ('is_looking_for_a_job', models.BooleanField(default=False)),
                ('professional_skills', models.TextField(blank=True)),
                ('fullname', models.CharField(max_length=150)),
                ('status', models.CharField(blank=True, max_length=70)),
                ('about_me', models.TextField(blank=True)),
            ],
            options={
                'verbose_name': 'profile',
                'verbose_name_plural': 'profiles',
                'db_table': 'profiles',
            },
        ),
        migrations.AddField(
            model_name='preferences',
            name='profile',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='profiles.profile'),
        ),
        migrations.AddField(
            model_name='photo',
            name='profile',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='profiles.profile'),
        ),
        migrations.AddField(
            model_name='contacts',
            name='profile',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='profiles.profile'),
        ),
    ]