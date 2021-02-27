# Generated by Django 3.1.7 on 2021-02-27 20:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photos',
            name='large',
            field=models.ImageField(default=None, null=True, upload_to='photos/large', verbose_name='large photo'),
        ),
        migrations.AlterField(
            model_name='photos',
            name='small',
            field=models.ImageField(default=None, null=True, upload_to='photos/small', verbose_name='small photo'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='about_me',
            field=models.TextField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='looking_for_a_job_description',
            field=models.TextField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='status',
            field=models.CharField(blank=True, default=None, max_length=300, null=True),
        ),
    ]
