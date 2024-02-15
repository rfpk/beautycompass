# Generated by Django 4.2.2 on 2023-09-06 11:21

import apps.tools.database_operations
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0056_alter_agerecommendation_slug_alter_keyaction_slug_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brandbanner',
            name='banner',
            field=apps.tools.database_operations.CleanImageField(blank=True, null=True, upload_to=apps.tools.database_operations.CleanImageField.get_image_path, verbose_name='Баннер'),
        ),
        migrations.AlterField(
            model_name='productbanner',
            name='banner',
            field=apps.tools.database_operations.CleanImageField(blank=True, null=True, upload_to=apps.tools.database_operations.CleanImageField.get_image_path, verbose_name='Баннер'),
        ),
        migrations.AlterField(
            model_name='seriesbanner',
            name='banner',
            field=apps.tools.database_operations.CleanImageField(blank=True, null=True, upload_to=apps.tools.database_operations.CleanImageField.get_image_path, verbose_name='Баннер'),
        ),
    ]