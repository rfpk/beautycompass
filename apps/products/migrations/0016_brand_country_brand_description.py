# Generated by Django 4.2.2 on 2023-07-24 15:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0002_auto_20230628_1602'),
        ('products', '0015_merge_20230718_0909'),
    ]

    operations = [
        migrations.AddField(
            model_name='brand',
            name='country',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='brands', to='settings.country', verbose_name='Страна'),
        ),
        migrations.AddField(
            model_name='brand',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Описание бренда'),
        ),
    ]
