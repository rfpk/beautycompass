# Generated by Django 4.2.2 on 2023-08-21 09:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0049_overviewcomment_is_publish_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='overviewcomment',
            options={},
        ),
        migrations.RemoveField(
            model_name='overviewcomment',
            name='is_publish',
        ),
    ]
