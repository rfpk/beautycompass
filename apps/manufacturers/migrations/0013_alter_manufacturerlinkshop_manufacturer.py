# Generated by Django 4.2.2 on 2023-07-25 10:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('manufacturers', '0012_manufacturerlinkshop_manufacturer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='manufacturerlinkshop',
            name='manufacturer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='manufacturer_links', to='manufacturers.manufacturer', verbose_name='Производитель'),
        ),
    ]
