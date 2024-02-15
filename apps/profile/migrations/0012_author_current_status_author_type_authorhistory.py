# Generated by Django 4.2.2 on 2023-07-28 12:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0011_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='current_status',
            field=models.CharField(choices=[('Активен', 'Активен'), ('Заблокирован на время', 'Заблокирован на время'), ('Заблокирован навсегда', 'Заблокирован навсегда')], default='Активен', max_length=55, verbose_name='Текущий статус активности'),
        ),
        migrations.AddField(
            model_name='author',
            name='type',
            field=models.CharField(choices=[('Читатель', 'Читатель'), ('Автор', 'Автор')], default='Читатель', max_length=55, verbose_name='Тип'),
        ),
        migrations.CreateModel(
            name='AuthorHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('Активен', 'Активен'), ('Заблокирован на время', 'Заблокирован на время'), ('Заблокирован навсегда', 'Заблокирован навсегда')], max_length=55, verbose_name='Статус пользователя')),
                ('created_at', models.DateTimeField(verbose_name='Дата начала действия статуса')),
                ('close_at', models.DateTimeField(verbose_name='Дата окончания действия статуса')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='history', to='profile.author', verbose_name='Автор')),
            ],
            options={
                'verbose_name': 'Журнал изменения статуса',
                'verbose_name_plural': 'Журнал изменений статусов',
            },
        ),
    ]