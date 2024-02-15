from django import forms

from apps.testing.models import QuestionTest, AnswerProfile
from apps.tools.database_operations import QuestionData

from django.utils.safestring import mark_safe, SafeText


def build_label(text: str, description: str) -> SafeText:
    """Generate Label Field"""
    description = description.replace(':', '')
    text = text.replace(':', '')
    if text and description:
        return mark_safe(f'<p class="text-uppercase">{text}:</p><small>{description}</small>')
    elif text:
        return mark_safe(f'<p class="text-uppercase">{text}:</p>')
    elif description:
        return mark_safe(f'<p class="text-uppercase">{description}:</p>')


def avg_words(words_list: list) -> int:
    """Find average of a list words"""
    length_words = [len(word) for word in words_list]
    return round(sum(length_words) / len(length_words))


class AnswerTestForm(forms.Form):
    def __init__(self, *args, **kwargs):
        test = kwargs.pop('test', None)
        super(AnswerTestForm, self).__init__(*args, **kwargs)
        questions = (QuestionTest.objects
                     .filter(test=test)
                     .select_related('test')
                     .prefetch_related('question_choices', 'question_choices__choice_images'))
        for question in questions:
            options = question.question_choices.all()
            choices = []
            for option in options:
                choices.append(
                    (option.pk, option.text, option.description, option.choice_images.all())
                )
            words = [el.text for el in options]
            avg_len_word = avg_words(words)
            if question.type in [QuestionData.QuestionTypeChoices.ONE, QuestionData.QuestionTypeChoices.BOOL]:
                self.fields[f'question_{question.id}'] = forms.ChoiceField(
                    label=build_label(question.text, question.description),
                    choices=choices,
                    widget=forms.RadioSelect(
                        attrs={
                            'class': f'''
                                                quest__resp radio__inpt {"" if avg_len_word > 9 or question.type.lower() == "bool" else "quest__adapt"}
                                            '''}
                    )
                )
            elif QuestionData.QuestionTypeChoices.MANY == question.type:
                self.fields[f'question_{question.id}'] = forms.MultipleChoiceField(
                    label=build_label(question.text, question.description),
                    choices=choices,
                    widget=forms.CheckboxSelectMultiple()
                )
            else:
                self.fields[f'question_{question.id}'] = forms.CharField(
                    label=build_label(question.text, question.description),
                    widget=forms.Textarea
                )

    def save_answers(self, user):
        from apps.profile.models import Profile
        for question_name, option_id in self.cleaned_data.items():
            if question_name.startswith('question_'):
                question_id = int(question_name.split('_')[1])

                answer = AnswerProfile.objects.create(
                    profile=Profile.objects.filter(user=user).first(),
                    question=QuestionTest.objects.filter(pk=question_id).first()
                )
                if answer.question.type == 'one':
                    answer.option.add(int(option_id))
                elif answer.question.type == 'many':
                    results = list(map(int, option_id))
                    answer.option.add(*results)
                else:
                    answer.text_answer = option_id
                answer.save()
