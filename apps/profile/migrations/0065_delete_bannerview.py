# Generated by Django 4.2.2 on 2023-08-29 11:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0064_bannerview_session_id'),
    ]

    operations = [
        migrations.DeleteModel(
            name='BannerView',
        ),
    ]
