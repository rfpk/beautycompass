# Generated by Django 4.2.2 on 2023-08-25 11:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manufacturers', '0027_manufacturerreviewanswer'),
    ]

    operations = [
        migrations.RenameField(
            model_name='manufacturerreviewanswer',
            old_name='profile',
            new_name='manufacturer',
        ),
    ]
