from django import forms

from apps.selection.models import QuestionSelection, AnswerSelectionProfile
from apps.tools.database_operations import QuestionData

from apps.testing.forms import build_label


class AnswerSelectionForm(forms.Form):
    def __init__(self, *args, **kwargs):
        selection = kwargs.pop('selection', None)
        super(AnswerSelectionForm, self).__init__(*args, **kwargs)
        questions = (QuestionSelection.objects
                     .filter(selection=selection)
                     .select_related('selection')
                     .prefetch_related('question_selection_options')
                     )
        for question in questions:
            options = question.question_selection_options.all()
            if QuestionData.QuestionTypeChoices.MANY == question.type:
                self.fields[f'question_{question.id}'] = forms.MultipleChoiceField(
                    label=question.text,
                    choices=[(option.pk, option.text) for option in options],
                    widget=forms.CheckboxSelectMultiple(attrs={
                        'class': 'form-select',
                    })
                )
            elif question.type in [QuestionData.QuestionTypeChoices.ONE, QuestionData.QuestionTypeChoices.BOOL]:
                self.fields[f'question_{question.id}'] = forms.ChoiceField(
                    label=build_label(question.text, question.description),
                    choices=[(option.pk, option.text) for option in options],
                    widget=forms.RadioSelect
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

                answer = AnswerSelectionProfile.objects.create(
                    profile=Profile.objects.filter(user=user).first(),
                    question=QuestionSelection.objects.filter(pk=question_id).first()
                )
                if answer.question.type == 'one' or answer.question.type == 'bool':
                    answer.option.add(int(option_id))
                elif answer.question.type == 'many':
                    results = list(map(int, option_id))
                    answer.option.add(*results)
                else:
                    answer.text_answer = option_id
                answer.save()
