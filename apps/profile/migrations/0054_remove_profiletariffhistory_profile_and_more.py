# Generated by Django 4.2.2 on 2023-08-22 08:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0053_profileservicehistory_end_date_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profiletariffhistory',
            name='profile',
        ),
        migrations.RemoveField(
            model_name='profiletariffhistory',
            name='tariff_plan',
        ),
        migrations.DeleteModel(
            name='ProfileServiceHistory',
        ),
        migrations.DeleteModel(
            name='ProfileTariffHistory',
        ),
    ]
