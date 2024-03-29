# Generated by Django 4.2.2 on 2023-07-10 10:40

import apps.tools.database_operations
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0011_product_rating_alter_review_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brand',
            name='image',
            field=apps.tools.database_operations.CleanImageField(blank=True, upload_to=apps.tools.database_operations.CleanImageField.get_image_path, verbose_name='Картинка'),
        ),
    ]
