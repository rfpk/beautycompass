# Generated by Django 4.2.2 on 2023-07-20 13:04

from django.db import migrations


class Migration(migrations.Migration):
    atomic = False

    dependencies = [
        ('selection', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Option',
            new_name='OptionSelection',
        ),
    ]
