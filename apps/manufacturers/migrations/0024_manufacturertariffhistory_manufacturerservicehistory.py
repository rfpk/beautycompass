# Generated by Django 4.2.2 on 2023-08-22 08:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0009_additionalservice_price'),
        ('manufacturers', '0023_remove_manufacturer_link_banner'),
    ]

    operations = [
        migrations.CreateModel(
            name='ManufacturerTariffHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField(auto_now_add=True, verbose_name='Начало действия')),
                ('end_date', models.DateField(blank=True, null=True, verbose_name='Окончание действия')),
                ('manufacturer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='manufacturer_tariffs', to='manufacturers.manufacturer', verbose_name='Производитель')),
                ('tariff_plan', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='tariff_manufacturers', to='services.tariff', verbose_name='Тарифный план')),
            ],
            options={
                'verbose_name': 'История тарифного плана',
                'verbose_name_plural': 'История тарифных планов',
            },
        ),
        migrations.CreateModel(
            name='ManufacturerServiceHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField(auto_now_add=True, verbose_name='Начало действия')),
                ('end_date', models.DateField(blank=True, null=True, verbose_name='Окончание действия')),
                ('manufacturer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='manufacturer_services', to='manufacturers.manufacturer', verbose_name='Производитель')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='service_manufacturers', to='services.additionalservice', verbose_name='Дополнительная услуга')),
            ],
            options={
                'verbose_name': 'История дополнительной услуги',
                'verbose_name_plural': 'История дополнительных услуг',
            },
        ),
    ]