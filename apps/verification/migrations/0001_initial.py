# Generated by Django 4.2.2 on 2023-07-02 18:35

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('profile', '0002_profile'),
    ]

    operations = [
        migrations.CreateModel(
            name='RegistrationLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=500)),
                ('count', models.PositiveIntegerField(default=0)),
                ('is_used', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('email', models.EmailField(max_length=254, verbose_name='email')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None)),
                ('nickname', models.CharField(blank=True, max_length=15)),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('profile', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='profile_registration_links', to='profile.profile')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]