# Generated by Django 4.2.2 on 2023-08-07 10:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('profile', '0033_ip_followingpageaction_ip_viewaction_ip'),
    ]

    operations = [
        migrations.CreateModel(
            name='Conversion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_action', models.PositiveIntegerField(choices=[(0, 'Удаление'), (1, 'Добавление')], default=1, verbose_name='Тип действия')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('object_id', models.PositiveIntegerField(null=True)),
                ('conversions_object_id', models.PositiveIntegerField(null=True)),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
                ('conversions_content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='content_type_conversions', to='contenttypes.contenttype')),
                ('ip', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ip_conversions', to='profile.ip', verbose_name='IP-aдрес')),
                ('profile', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='profile_conversions', to='profile.profile', verbose_name='Профиль')),
            ],
            options={
                'verbose_name': 'История переходов на страницу продукта/статьи/бренда/',
                'verbose_name_plural': 'История переходов на страницы продуктов/статей/брендов/',
            },
        ),
        migrations.DeleteModel(
            name='FollowingPageAction',
        ),
    ]
