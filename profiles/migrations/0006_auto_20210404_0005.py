# Generated by Django 3.1.7 on 2021-04-03 21:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0005_auto_20210403_2359'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='status',
            field=models.CharField(blank=True, default='', max_length=300),
        ),
    ]
