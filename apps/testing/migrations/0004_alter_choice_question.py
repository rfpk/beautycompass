# Generated by Django 4.2.2 on 2023-07-19 08:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('testing', '0003_alter_choice_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='choice',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='question_choices', to='testing.questiontest', verbose_name='Вопрос'),
        ),
    ]
