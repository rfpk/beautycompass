# Generated by Django 4.2.2 on 2023-07-25 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0021_keyaction_keyasset_sex_product_composition_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='pricecategory',
            name='slug',
            field=models.SlugField(blank=True, null=True, unique=True),
        ),
    ]