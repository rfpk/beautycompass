# Generated by Django 4.2.2 on 2023-09-26 14:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0003_blockcomment'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blockcomment',
            options={'verbose_name': 'Тип блокировки комментария', 'verbose_name_plural': 'Типы блокировок комментариев'},
        ),
    ]
