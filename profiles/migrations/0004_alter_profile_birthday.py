# Generated by Django 3.2.1 on 2021-10-01 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_auto_20210823_0219'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='birthday',
            field=models.DateField(blank=True, null=True),
        ),
    ]
