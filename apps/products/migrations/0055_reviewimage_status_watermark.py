# Generated by Django 4.2.2 on 2023-09-04 07:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0054_alter_series_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='reviewimage',
            name='status_watermark',
            field=models.BooleanField(default=False, verbose_name='Необходим копирайт'),
        ),
    ]
