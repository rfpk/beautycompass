# Generated by Django 4.2.2 on 2023-07-12 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_article_profile_view'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='views',
            field=models.PositiveIntegerField(default=0, verbose_name='Просмотры'),
        ),
    ]
