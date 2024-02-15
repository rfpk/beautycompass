# Generated by Django 4.2.2 on 2023-07-18 11:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0007_alter_answer_product_alter_answer_question_and_more'),
        ('manufacturers', '0007_remove_manufacturer_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='manufacturer',
            name='profile',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='profile.profile', verbose_name='Профиль'),
        ),
    ]
