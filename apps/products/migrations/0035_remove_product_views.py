# Generated by Django 4.2.2 on 2023-08-07 08:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0034_merge_20230804_1323'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='views',
        ),
    ]
