# Generated by Django 4.0.6 on 2022-08-08 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_alter_profile_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='following',
            field=models.IntegerField(default=0),
        ),
    ]
