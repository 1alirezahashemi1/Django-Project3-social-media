# Generated by Django 4.1 on 2022-08-04 09:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="profile", old_name="username", new_name="name",
        ),
    ]
