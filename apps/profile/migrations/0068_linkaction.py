# Generated by Django 4.2.2 on 2023-08-31 11:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('profile', '0067_rename_author_gratitude_gratitudeaction_author_action_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='LinkAction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_action', models.PositiveIntegerField(choices=[(0, 'Удаление'), (1, 'Добавление')], default=1, null=True, verbose_name='Тип действия')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('object_id', models.PositiveIntegerField(null=True)),
                ('session_id', models.CharField(blank=True, max_length=150, null=True, verbose_name='Сессия пользователя')),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
                ('ip', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ip_links', to='profile.ip', verbose_name='IP-aдрес')),
                ('profile', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='profile_links_actions', to='profile.profile', verbose_name='Профиль')),
            ],
            options={
                'verbose_name': 'История переходов по ссылкам на источники',
                'verbose_name_plural': 'История переходов по ссылкам на источники',
            },
        ),
    ]
