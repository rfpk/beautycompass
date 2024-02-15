# Generated by Django 4.2.2 on 2023-08-09 16:22

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('programs', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='program',
            name='description',
            field=tinymce.models.HTMLField(blank=True, verbose_name='Описание программы'),
        ),
    ]
