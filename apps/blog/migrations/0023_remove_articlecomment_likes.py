# Generated by Django 4.2.2 on 2023-08-18 12:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0022_article_tag'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='articlecomment',
            name='likes',
        ),
    ]
