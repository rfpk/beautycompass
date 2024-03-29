# Generated by Django 4.2.2 on 2023-07-05 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0002_profile'),
        ('blog', '0006_article_profile_like'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='profile_like',
            field=models.ManyToManyField(blank=True, null=True, related_name='profile_like_articles', to='profile.profile'),
        ),
    ]
