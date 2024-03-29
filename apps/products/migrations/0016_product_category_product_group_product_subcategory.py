# Generated by Django 4.2.2 on 2023-07-21 11:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
        ('products', '0015_merge_20230718_0909'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='catalog.category', verbose_name='Рейтинг продукта'),
        ),
        migrations.AddField(
            model_name='product',
            name='group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='catalog.cataloggroup', verbose_name='Рейтинг продукта'),
        ),
        migrations.AddField(
            model_name='product',
            name='subcategory',
            field=models.ManyToManyField(blank=True, to='catalog.subcategory', verbose_name='Рейтинг продукта'),
        ),
    ]
