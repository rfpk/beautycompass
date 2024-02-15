# Generated by Django 4.2.2 on 2023-11-10 02:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0008_hairtype_skintype'),
        ('profile', '0074_overviewcomment_block_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='contact_email',
            field=models.EmailField(blank=True, max_length=254, null=True, verbose_name='Контактный email'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='email',
            field=models.EmailField(max_length=254, null=True, unique=True, verbose_name='email address'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='hair_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='settings.hairtype', verbose_name='Тип волос'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='public_email',
            field=models.EmailField(blank=True, max_length=254, null=True, verbose_name='Публичный email'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='sex',
            field=models.CharField(blank=True, choices=[('M', 'Мужчина'), ('F', 'Женщина')], max_length=1, null=True, verbose_name='Пол'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='skin_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='settings.skintype', verbose_name='Тип кожи'),
        ),
    ]
