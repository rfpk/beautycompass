# Generated by Django 4.2.2 on 2023-07-28 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0014_alter_authorhistory_close_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='rating',
            field=models.PositiveIntegerField(default=0, verbose_name='Рейтинг'),
        ),
    ]