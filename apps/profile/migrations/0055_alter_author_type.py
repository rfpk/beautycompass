# Generated by Django 4.2.2 on 2023-08-24 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0054_remove_profiletariffhistory_profile_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='type',
            field=models.CharField(choices=[('R', 'Читатель'), ('A', 'Автор')], default='R', max_length=25, verbose_name='Тип пользователя'),
        ),
    ]
