# Generated by Django 4.2.2 on 2023-08-31 09:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manufacturers', '0031_alter_manufacturerlinkshop_name_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='manufacturerlinkshop',
            options={'verbose_name': 'Ссылка на магазины производителя', 'verbose_name_plural': 'Ссылки на магазины производителей'},
        ),
    ]
