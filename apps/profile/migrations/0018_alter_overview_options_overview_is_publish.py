# Generated by Django 4.2.2 on 2023-07-28 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0017_overview_overviewphoto'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='overview',
            options={'verbose_name': 'Обзор', 'verbose_name_plural': 'Обзоры'},
        ),
        migrations.AddField(
            model_name='overview',
            name='is_publish',
            field=models.BooleanField(default=False, verbose_name='Опубликовать'),
        ),
    ]
