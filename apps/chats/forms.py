from django import forms

from apps.chats.models import Message, ConversationPost, CommentConversation, ImageComment, ImagePost
from apps.products.models import Tag


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['title', 'text', 'sender', 'receiver']


class ConversationForm(forms.ModelForm):
    tag = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(), required=False)

    class Meta:
        model = ConversationPost
        fields = ['title', 'text', 'tag']
        labels = {
            'title': 'Заголовок поста',
            'text': 'Текст',
            'tag': 'Теги'
        }

class CreateCommentForm(forms.ModelForm):
    images = forms.FileField(label='Изображения серии', required=False,
                             widget=forms.ClearableFileInput(attrs={"allow_multiple_selected": True}))
    post = forms.IntegerField(widget=forms.HiddenInput)
    parent = forms.IntegerField(widget=forms.HiddenInput, required=False)

    def save(self, commit=True):
        comment = super().save(commit=False)
        return comment
    
    def check_exist(self, user):
        parent = self.cleaned_data.get('parent', None)
        if parent:
            comment_exist = CommentConversation.objects.filter(
                author__profile__user=user,
                pk=int(parent)
            ).first()
            return comment_exist

    class Meta:
        model = CommentConversation
        fields = ['text', ]
        labels = {
            'text': 'Текст',
        }

