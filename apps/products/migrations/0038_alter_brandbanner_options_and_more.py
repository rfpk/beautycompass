# Generated by Django 4.2.2 on 2023-08-09 07:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0037_brandbanner_banner_productbanner_banner_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='brandbanner',
            options={'verbose_name': 'Баннер', 'verbose_name_plural': 'Баннеры'},
        ),
        migrations.AlterModelOptions(
            name='productbanner',
            options={'verbose_name': 'Баннер', 'verbose_name_plural': 'Баннеры'},
        ),
        migrations.AlterModelOptions(
            name='seriesbanner',
            options={'verbose_name': 'Баннер', 'verbose_name_plural': 'Баннеры'},
        ),
    ]
