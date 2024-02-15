# Generated by Django 4.2.2 on 2023-07-20 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tariff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.CharField(choices=[('to 10', 'до 10'), ('to 50', 'до 50'), ('to 200', 'до 200'), ('to 1000', 'до 1000'), ('over 1000', 'более 1000')], max_length=20, verbose_name='Количество средств в каталоге')),
                ('period', models.CharField(choices=[(3, '3 месяца'), (6, '6 месяцев'), (12, '12 месяцев')], max_length=20, verbose_name='Период')),
                ('price', models.PositiveIntegerField(verbose_name='Цена тарифа')),
            ],
            options={
                'verbose_name': 'Тариф',
                'verbose_name_plural': 'Тарифы',
            },
        ),
    ]
