# Generated by Django 4.2.2 on 2023-08-10 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0042_remove_profile_services'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Активен'),
        ),
    ]
