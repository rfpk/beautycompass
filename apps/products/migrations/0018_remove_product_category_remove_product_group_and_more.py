# Generated by Django 4.2.2 on 2023-07-24 10:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0017_alter_product_category_alter_product_group_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='category',
        ),
        migrations.RemoveField(
            model_name='product',
            name='group',
        ),
        migrations.RemoveField(
            model_name='product',
            name='subcategory',
        ),
    ]