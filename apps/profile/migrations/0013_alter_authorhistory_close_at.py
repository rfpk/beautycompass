# Generated by Django 4.2.2 on 2023-07-28 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0012_author_current_status_author_type_authorhistory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='authorhistory',
            name='close_at',
            field=models.DateTimeField(blank=True, verbose_name='Дата окончания действия статуса'),
        ),
    ]
