# Generated by Django 4.2.2 on 2023-08-10 12:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0041_alter_profileservicehistory_start_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='services',
        ),
    ]