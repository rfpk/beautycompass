# Generated by Django 4.2.2 on 2023-10-11 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0077_remove_review_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='rating',
            field=models.FloatField(blank=True, default=0, null=True, verbose_name='Рейтинг'),
        ),
    ]
