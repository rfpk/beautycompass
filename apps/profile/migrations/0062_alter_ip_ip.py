# Generated by Django 4.2.2 on 2023-08-29 07:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0061_alter_ip_ip'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ip',
            name='ip',
            field=models.GenericIPAddressField(unique=True),
        ),
    ]
