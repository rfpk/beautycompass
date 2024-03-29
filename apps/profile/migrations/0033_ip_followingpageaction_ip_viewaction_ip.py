# Generated by Django 4.2.2 on 2023-08-07 07:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0032_followingpageaction'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'IP-aдрес',
                'verbose_name_plural': 'IP-aдреса',
            },
        ),
        migrations.AddField(
            model_name='followingpageaction',
            name='ip',
            field=models.ForeignKey(default=123, on_delete=django.db.models.deletion.CASCADE, related_name='ip_followings', to='profile.ip', verbose_name='IP-aдрес'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='viewaction',
            name='ip',
            field=models.ForeignKey(default=123, on_delete=django.db.models.deletion.CASCADE, related_name='ip_views', to='profile.ip', verbose_name='IP-aдрес'),
            preserve_default=False,
        ),
    ]
