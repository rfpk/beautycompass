from django.db import models

from apps.tools.database_operations import TestData, QuestionData, OptionData, AnswerData


class Selection(TestData):
    """Model for create selection"""

    class Meta:
        verbose_name = 'Подбор'
        verbose_name_plural = 'Подборы'


class QuestionSelection(QuestionData):
    """Model for create selection question"""
    selection = models.ForeignKey(Selection, on_delete=models.CASCADE,
                                  related_name='selection_questions', verbose_name='Подбор')

class OptionSelection(OptionData):
    """Class for create choice of answer on question selection"""
    question = models.ForeignKey(QuestionSelection, on_delete=models.CASCADE,
                                 related_name='question_selection_options', verbose_name='Вопрос')


class AnswerSelectionProfile(AnswerData):
    """Class for save answers of profile on selection"""
    profile = models.ForeignKey('profile.Profile', on_delete=models.CASCADE,
                                related_name='profile_selection_answers', verbose_name='Профиль')
    question = models.ForeignKey(QuestionSelection, on_delete=models.CASCADE, verbose_name='Вопрос',
                                 blank=True, null=True)

    option = models.ManyToManyField(OptionSelection, related_name='option_selection_answers',
                                    verbose_name='Выбранные ответы', blank=True)

    def __str__(self):
        return f'{self.profile}'

