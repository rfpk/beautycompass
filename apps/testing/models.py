from django.db import models

from apps.tools.database_operations import CleanImageField, TestData, QuestionData, OptionData, AnswerData
from apps.profile.models import Profile


class Test(TestData):
    """Model for create test"""
    class Meta:
        verbose_name = 'Тест'
        verbose_name_plural = 'Тесты'


class QuestionTest(QuestionData):
    """Model for create question"""
    test = models.ForeignKey(Test, on_delete=models.CASCADE,
                             related_name='test_questions', verbose_name='Тест')

class Option(OptionData):
    """Class for create choice of answer on question"""
    question = models.ForeignKey(QuestionTest, on_delete=models.CASCADE,
                                 related_name='question_choices', verbose_name='Вопрос')
    recomendation = models.TextField(verbose_name='Рекомендация', blank=True, null=True)


class ImageOption(models.Model):
    """Class for add image to choice of answer"""
    image = CleanImageField(upload_to='testing/images/', verbose_name='Картинка',
                            blank=True, null=True)
    option = models.ForeignKey(Option, on_delete=models.CASCADE, blank=True, null=True,
                               related_name='choice_images', verbose_name='Вариант ответа')


class TestsResult(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='profile_test_result', verbose_name='Профиль')
    name = models.CharField(max_length=255, null=True, verbose_name='Название Теста')
    created_at = models.DateField(auto_now_add=True, blank=True, null=True, verbose_name='Время создания')
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)
    
    class Meta:
        verbose_name = 'Результат Теста'
        verbose_name_plural = 'Результаты Тестов'


class AnswerProfile(AnswerData):
    """Class for save answers of profile"""
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE,
                                related_name='profile_test_answers', verbose_name='Профиль')
    question = models.ForeignKey(QuestionTest, on_delete=models.CASCADE, verbose_name='Вопрос',
                                 blank=True, null=True)
    option = models.ManyToManyField(Option, related_name='choice_answers',
                                    verbose_name='Выбранные ответы', blank=True)
    test_result_user = models.CharField(max_length=255, null=True, verbose_name='Название Теста')

    def __str__(self):
        return f'{self.profile}'
