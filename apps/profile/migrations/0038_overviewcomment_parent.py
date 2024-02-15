# Generated by Django 4.2.2 on 2023-08-17 08:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0037_rename_subscribers_author_subscriber'),
    ]

    operations = [
        migrations.AddField(
            model_name='overviewcomment',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='profile.overviewcomment', verbose_name='Корневой комментарий'),
        ),
    ]