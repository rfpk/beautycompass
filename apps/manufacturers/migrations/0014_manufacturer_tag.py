# Generated by Django 4.2.2 on 2023-07-26 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0027_brand_tag_series_tag_alter_product_tag'),
        ('manufacturers', '0013_alter_manufacturerlinkshop_manufacturer'),
    ]

    operations = [
        migrations.AddField(
            model_name='manufacturer',
            name='tag',
            field=models.ManyToManyField(blank=True, related_name='manufacturer_tags', to='products.tag', verbose_name='Теги'),
        ),
    ]