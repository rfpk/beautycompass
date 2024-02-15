# Generated by Django 4.2.2 on 2023-08-10 12:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0009_additionalservice_price'),
        ('profile', '0039_alter_profile_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProfileServiceHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField(auto_now_add=True)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='profile_services', to='profile.profile', verbose_name='Профиль')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='service_profiles', to='services.additionalservice', verbose_name='Дополнительная услуга')),
            ],
        ),
    ]