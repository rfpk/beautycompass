# Generated by Django 4.2.2 on 2023-07-07 09:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0002_profile'),
        ('products', '0009_alter_review_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='profile',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='profile_reviews', to='profile.profile', verbose_name='Отзыв пользователя'),
        ),
    ]
