# Generated by Django 4.2.2 on 2023-08-01 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0022_alter_author_current_status_alter_author_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='overviewcomment',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]