# Generated by Django 4.0.6 on 2022-08-09 10:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_comment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='authorr',
            new_name='author',
        ),
    ]
