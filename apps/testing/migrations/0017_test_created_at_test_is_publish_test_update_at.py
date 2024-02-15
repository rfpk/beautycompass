# Generated by Django 4.2.2 on 2023-07-24 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testing', '0016_alter_questiontest_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='test',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='Дата создания'),
        ),
        migrations.AddField(
            model_name='test',
            name='is_publish',
            field=models.BooleanField(default=False, verbose_name='Опубликовать'),
        ),
        migrations.AddField(
            model_name='test',
            name='update_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Дата обновления'),
        ),
    ]
