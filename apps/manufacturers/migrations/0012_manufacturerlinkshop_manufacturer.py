# Generated by Django 4.2.2 on 2023-07-25 10:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('manufacturers', '0011_rename_linkshop_manufacturerlinkshop_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='manufacturerlinkshop',
            name='manufacturer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='manufacturers.manufacturer', verbose_name='Производитель'),
        ),
    ]