# Generated by Django 4.2.2 on 2023-07-27 08:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0026_brand_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='series',
            name='slug',
            field=models.SlugField(blank=True, unique=True),
        ),
    ]
