# Generated by Django 4.2.2 on 2023-08-31 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0053_alter_brandlink_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='series',
            name='slug',
            field=models.SlugField(unique=True),
        ),
    ]
