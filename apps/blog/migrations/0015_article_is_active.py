# Generated by Django 4.2.2 on 2023-07-27 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0014_article_is_draft_article_is_publish'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Активна'),
        ),
    ]