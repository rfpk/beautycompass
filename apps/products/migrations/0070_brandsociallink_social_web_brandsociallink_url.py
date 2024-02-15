# Generated by Django 4.2.2 on 2023-10-02 09:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0005_socialweb'),
        ('products', '0069_remove_brandsociallink_social_web'),
    ]

    operations = [
        migrations.AddField(
            model_name='brandsociallink',
            name='social_web',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='settings.socialweb', verbose_name='Социальная сеть'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='brandsociallink',
            name='url',
            field=models.URLField(default=1, max_length=500, verbose_name='Ccылка на социальную сеть'),
            preserve_default=False,
        ),
    ]