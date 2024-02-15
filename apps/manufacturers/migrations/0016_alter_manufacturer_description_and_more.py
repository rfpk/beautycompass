# Generated by Django 4.2.2 on 2023-08-09 15:46

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('manufacturers', '0015_merge_0014_manufacturer_tag_0014_merge_20230725_1348'),
    ]

    operations = [
        migrations.AlterField(
            model_name='manufacturer',
            name='description',
            field=tinymce.models.HTMLField(blank=True, verbose_name='Краткое описание компании'),
        ),
        migrations.AlterField(
            model_name='manufacturer',
            name='history',
            field=tinymce.models.HTMLField(blank=True, verbose_name='История компании'),
        ),
        migrations.AlterField(
            model_name='manufacturer',
            name='principle',
            field=tinymce.models.HTMLField(blank=True, verbose_name='Принципы компании'),
        ),
    ]