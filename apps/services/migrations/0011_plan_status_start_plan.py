# Generated by Django 4.2.2 on 2023-08-22 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0010_alter_plan_period'),
    ]

    operations = [
        migrations.AddField(
            model_name='plan',
            name='status_start_plan',
            field=models.BooleanField(default=1, verbose_name='План для стартового периода'),
            preserve_default=False,
        ),
    ]
