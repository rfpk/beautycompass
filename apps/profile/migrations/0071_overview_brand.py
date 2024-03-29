# Generated by Django 4.2.2 on 2023-09-05 15:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0056_alter_agerecommendation_slug_alter_keyaction_slug_and_more'),
        ('profile', '0070_overview_tag'),
    ]

    operations = [
        migrations.AddField(
            model_name='overview',
            name='brand',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='brand_overviews', to='products.brand', verbose_name='Бренд'),
        ),
    ]
