# Generated by Django 4.2.2 on 2023-08-24 09:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0054_remove_profiletariffhistory_profile_and_more'),
        ('chats', '0019_alter_chat_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='chat',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chat_messages', to='chats.chat', verbose_name='Чат'),
        ),
        migrations.AlterField(
            model_name='message',
            name='date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата отправления'),
        ),
        migrations.AlterField(
            model_name='message',
            name='receiver',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='receiver_messages', to='profile.profile', verbose_name='Получатель'),
        ),
        migrations.AlterField(
            model_name='message',
            name='sender',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sender_messages', to='profile.profile', verbose_name='Отправитель'),
        ),
        migrations.AlterField(
            model_name='message',
            name='text',
            field=models.TextField(verbose_name='Текст'),
        ),
        migrations.AlterField(
            model_name='message',
            name='title',
            field=models.CharField(blank=True, max_length=300, verbose_name='Тема сообщения'),
        ),
    ]
