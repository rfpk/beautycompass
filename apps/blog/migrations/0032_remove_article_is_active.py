# Generated by Django 4.2.2 on 2023-09-21 06:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0031_articlecomment_is_publish'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='is_active',
        ),
    ]
