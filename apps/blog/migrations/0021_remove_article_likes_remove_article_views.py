# Generated by Django 4.2.2 on 2023-08-07 10:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0020_merge_20230804_1323'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='likes',
        ),
        migrations.RemoveField(
            model_name='article',
            name='views',
        ),
    ]
