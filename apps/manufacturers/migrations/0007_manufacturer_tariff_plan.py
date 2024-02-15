# Generated by Django 4.2.2 on 2023-07-20 10:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0001_initial'),
        ('manufacturers', '0006_alter_linkshop_options_alter_manufacturer_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='manufacturer',
            name='tariff_plan',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='tariff_manufacturers', to='services.tariff', verbose_name='Тариф'),
        ),
    ]
