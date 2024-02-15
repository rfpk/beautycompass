# Generated by Django 4.2.2 on 2023-08-21 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0051_alter_overviewcomment_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bannerview',
            name='type_action',
            field=models.PositiveIntegerField(choices=[(0, 'Удаление'), (1, 'Добавление')], default=1, null=True, verbose_name='Тип действия'),
        ),
        migrations.AlterField(
            model_name='conversion',
            name='type_action',
            field=models.PositiveIntegerField(choices=[(0, 'Удаление'), (1, 'Добавление')], default=1, null=True, verbose_name='Тип действия'),
        ),
        migrations.AlterField(
            model_name='favoriteaction',
            name='type_action',
            field=models.PositiveIntegerField(choices=[(0, 'Удаление'), (1, 'Добавление')], default=1, null=True, verbose_name='Тип действия'),
        ),
        migrations.AlterField(
            model_name='likeaction',
            name='type_action',
            field=models.PositiveIntegerField(choices=[(0, 'Удаление'), (1, 'Добавление')], default=1, null=True, verbose_name='Тип действия'),
        ),
        migrations.AlterField(
            model_name='viewaction',
            name='type_action',
            field=models.PositiveIntegerField(choices=[(0, 'Удаление'), (1, 'Добавление')], default=1, null=True, verbose_name='Тип действия'),
        ),
    ]