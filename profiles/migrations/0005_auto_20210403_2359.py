# Generated by Django 3.1.7 on 2021-04-03 20:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0004_auto_20210228_0018'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='status',
            field=models.CharField(blank=True, default=None, max_length=300),
        ),
    ]