# Generated by Django 4.2.2 on 2023-07-04 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_reviewimage'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='mark',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]