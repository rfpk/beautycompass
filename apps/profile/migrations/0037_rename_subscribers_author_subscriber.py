# Generated by Django 4.2.2 on 2023-08-08 10:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0036_remove_author_count_gratitude_author_gratitude'),
    ]

    operations = [
        migrations.RenameField(
            model_name='author',
            old_name='subscribers',
            new_name='subscriber',
        ),
    ]
