# Generated by Django 4.2.2 on 2023-07-26 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0025_merge_20230725_1341'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='views',
            field=models.PositiveIntegerField(default=0, verbose_name='Просмотры средства'),
        ),
    ]
