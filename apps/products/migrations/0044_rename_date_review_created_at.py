# Generated by Django 4.2.2 on 2023-08-14 11:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0043_merge_20230814_0900'),
    ]

    operations = [
        migrations.RenameField(
            model_name='review',
            old_name='date',
            new_name='created_at',
        ),
    ]