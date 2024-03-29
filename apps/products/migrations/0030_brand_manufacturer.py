# Generated by Django 4.2.2 on 2023-08-02 14:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('manufacturers', '0014_merge_20230725_1348'),
        ('products', '0029_merge_20230801_1056'),
    ]

    operations = [
        migrations.AddField(
            model_name='brand',
            name='manufacturer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Manufacturer_brands', to='manufacturers.manufacturer', verbose_name='Производитель'),
        ),
    ]
