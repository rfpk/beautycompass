# Generated by Django 4.2.2 on 2023-07-19 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testing', '0012_answerprofile_text_answer_alter_answerprofile_choice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questiontest',
            name='type',
            field=models.PositiveIntegerField(choices=[('one', 'Один подходящий ответ'), ('many', 'Множественный выбор'), ('text', 'Свободная форма ответа')], verbose_name='Тип ответа'),
        ),
    ]
