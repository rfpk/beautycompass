# Generated by Django 4.2.2 on 2023-10-11 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0075_product_new_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='rating',
            field=models.PositiveIntegerField(default=0, verbose_name='Рейтинг'),
        ),
    ]
