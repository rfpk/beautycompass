# Generated by Django 4.2.2 on 2023-09-18 11:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chats', '0021_conversationpost_tag'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commentconversation',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='chats.conversationpost', verbose_name='Пост'),
        ),
    ]
