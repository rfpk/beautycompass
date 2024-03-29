# Generated by Django 4.2.2 on 2023-12-06 18:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0075_alter_profile_contact_email_alter_profile_email_and_more'),
        ('products', '0081_brandsubscriber'),
        ('programs', '0003_alter_complex_program'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='complex',
            name='products',
        ),
        migrations.RemoveField(
            model_name='program',
            name='description',
        ),
        migrations.RemoveField(
            model_name='program',
            name='text_appeal',
        ),
        migrations.AddField(
            model_name='program',
            name='is_publish',
            field=models.BooleanField(default=False, verbose_name='Опубликовать'),
        ),
        migrations.CreateModel(
            name='ProgramResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, null=True, verbose_name='Название Программы')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='profile_program_result', to='profile.profile', verbose_name='Профиль')),
                ('program', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='program_complexes_result', to='programs.program', verbose_name='Программа')),
            ],
            options={
                'verbose_name': 'Результат Программы',
                'verbose_name_plural': 'Результаты Программ',
            },
        ),
        migrations.CreateModel(
            name='ComplexResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Название комплекса')),
                ('recommendation', models.TextField(blank=True, max_length=255, verbose_name='Описание рекомендаций')),
                ('products', models.ManyToManyField(related_name='complexes_result', to='products.product', verbose_name='Продукты')),
                ('program', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='program_complex_result', to='programs.programresult', verbose_name='Программа')),
            ],
            options={
                'verbose_name': 'Комплекс Результат Программы',
                'verbose_name_plural': 'Комплексы Результатов Программ',
            },
        ),
    ]
