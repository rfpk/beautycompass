# Generated by Django 4.2.2 on 2023-07-18 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0005_alter_profile_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='is_active',
            field=models.BooleanField(blank=True, default=True, null=True, verbose_name='Активен'),
        ),
    ]