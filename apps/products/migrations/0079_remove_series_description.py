# Generated by Django 4.2.2 on 2023-10-24 08:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0078_review_rating'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='series',
            name='description',
        ),
    ]
