# Generated by Django 4.2.2 on 2023-08-10 16:54

from django.db import migrations, models
import django.db.models.deletion
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0037_rename_subscribers_author_subscriber'),
        ('chats', '0002_remove_message_profile_get_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConversationPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=300, verbose_name='Заголовок поста')),
                ('text', tinymce.models.HTMLField(blank=True, verbose_name='Текст поста')),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('is_publish', models.BooleanField(default=True)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='profile_conversation_posts', to='profile.profile')),
            ],
            options={
                'verbose_name': 'Пост беседки',
                'verbose_name_plural': 'Посты беседки',
            },
        ),
    ]
