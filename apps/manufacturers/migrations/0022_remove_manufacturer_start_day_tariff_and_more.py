# Generated by Django 4.2.2 on 2023-08-22 08:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manufacturers', '0021_answerreview_is_publish_answerreview_text_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='manufacturer',
            name='start_day_tariff',
        ),
        migrations.RemoveField(
            model_name='manufacturer',
            name='tariff_plan',
        ),
    ]
