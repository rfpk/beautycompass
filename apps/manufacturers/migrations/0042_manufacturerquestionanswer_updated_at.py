# Generated by Django 4.2.2 on 2023-10-26 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manufacturers', '0041_remove_manufacturerquestionanswer_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='manufacturerquestionanswer',
            name='updated_at',
            field=models.DateField(auto_now=True, verbose_name='Время последнего редактирования'),
        ),
    ]