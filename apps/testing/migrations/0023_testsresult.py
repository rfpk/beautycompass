# Generated by Django 4.2.2 on 2023-12-01 04:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0075_alter_profile_contact_email_alter_profile_email_and_more'),
        ('testing', '0022_answerprofile_test_result_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestsResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, null=True, verbose_name='Название Теста')),
                ('created_at', models.DateField(auto_now_add=True, null=True, verbose_name='Время создания')),
                ('slug', models.SlugField(blank=True, max_length=255, null=True, unique=True)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='profile_test_result', to='profile.profile', verbose_name='Профиль')),
            ],
            options={
                'verbose_name': 'Результат Теста',
                'verbose_name_plural': 'Результаты Тестов',
            },
        ),
    ]
