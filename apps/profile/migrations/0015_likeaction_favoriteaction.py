# Generated by Django 4.2.2 on 2023-07-31 14:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('profile', '0014_remove_profile_favorite_articles_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='LikeAction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_action', models.PositiveIntegerField(blank=True, choices=[(0, 'Удаление'), (1, 'Добавление')], verbose_name='Тип действия')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('object_id', models.PositiveIntegerField(null=True)),
                ('content_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='profile_likes_actions', to='profile.profile', verbose_name='Профиль')),
            ],
            options={
                'verbose_name': 'История лайков пользователя',
                'verbose_name_plural': 'История лайков пользователей',
            },
        ),
        migrations.CreateModel(
            name='FavoriteAction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_action', models.PositiveIntegerField(blank=True, choices=[(0, 'Удаление'), (1, 'Добавление')], verbose_name='Тип действия')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('object_id', models.PositiveIntegerField(null=True)),
                ('content_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='profile_favorites_actions', to='profile.profile', verbose_name='Профиль')),
            ],
            options={
                'verbose_name': 'История добавления в избранное пользователя',
                'verbose_name_plural': 'История добавлений в избранное пользователей',
            },
        ),
    ]
