# Generated by Django 4.2.2 on 2023-07-21 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landing', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cooperation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=255, verbose_name='Заголовок страницы')),
                ('content', models.TextField(blank=True, verbose_name='Содержимое страницы')),
            ],
            options={
                'verbose_name': 'Сотрудничество',
                'verbose_name_plural': 'Сотрудничество',
            },
        ),
    ]