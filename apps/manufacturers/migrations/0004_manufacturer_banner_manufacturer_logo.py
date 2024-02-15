# Generated by Django 4.2.2 on 2023-07-14 10:07

import apps.tools.database_operations
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manufacturers', '0003_alter_manufacturer_email_alter_manufacturer_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='manufacturer',
            name='banner',
            field=apps.tools.database_operations.CleanImageField(blank=True, null=True, upload_to=apps.tools.database_operations.CleanImageField.get_image_path, verbose_name='Баннер'),
        ),
        migrations.AddField(
            model_name='manufacturer',
            name='logo',
            field=apps.tools.database_operations.CleanImageField(blank=True, null=True, upload_to=apps.tools.database_operations.CleanImageField.get_image_path, verbose_name='Логотип'),
        ),
    ]
