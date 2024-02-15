# Generated by Django 4.2.2 on 2023-08-04 14:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('profile', '0030_alter_favoriteaction_type_action_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ViewAction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_action', models.PositiveIntegerField(choices=[(0, 'Удаление'), (1, 'Добавление')], default=1, verbose_name='Тип действия')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('object_id', models.PositiveIntegerField(null=True)),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
                ('profile', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='profile_views_actions', to='profile.profile', verbose_name='Профиль')),
            ],
            options={
                'verbose_name': 'История просмотров',
                'verbose_name_plural': 'История просмотров',
            },
        ),
    ]