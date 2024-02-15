# Generated by Django 4.2.2 on 2023-07-24 07:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('landing', '0003_delete_about_delete_contact_delete_cooperation'),
    ]

    operations = [
        migrations.CreateModel(
            name='TypePage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=50, verbose_name='Тип страницы')),
            ],
            options={
                'verbose_name': 'Тип основной страницы',
                'verbose_name_plural': 'Типы основных страниц',
            },
        ),
        migrations.CreateModel(
            name='MainPage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=255, verbose_name='Заголовок страницы')),
                ('content', models.TextField(blank=True, verbose_name='Содержимое страницы')),
                ('slug', models.SlugField(unique=True)),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='landing.typepage', verbose_name='Тип страницы')),
            ],
            options={
                'verbose_name': 'Основная страница',
                'verbose_name_plural': 'Основные страницы',
            },
        ),
    ]