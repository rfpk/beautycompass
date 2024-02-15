from django import forms

from apps.blog.models import Article, ArticlePhoto, ArticleComment, Complaint
from apps.products.models import Tag, Brand

from apps.profile.models import OverviewComment
from apps.chats.models import CommentConversation

class ArticleForm(forms.ModelForm):
    button_clicked = forms.CharField(widget=forms.HiddenInput(), initial='', required=False)
    images = forms.FileField(label='Фотографии статьи', required=False,
                             widget=forms.ClearableFileInput(attrs={"allow_multiple_selected": True}))
    brand = forms.ModelChoiceField(queryset=Brand.objects.all(), required=False)
    tag = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(), required=False)

    class Meta:
        model = Article
        fields = ["title", "text", "thumbnail", "brand", "tag"]

        labels = {
            'title': 'Заголовок статьи',
            'text': 'Текст статьи',
            'thumbnail': 'Главное фото',
            'brand': 'Бренд',
            'tag': 'Теги',
        }

    def save(self, commit=True):
        article = super().save(commit=commit)
        images = self.cleaned_data.get('images')
        if images:
            for image in images:
                ArticlePhoto.objects.create(article=article, image=image)
        if self.cleaned_data.get('button_clicked') == 'publish':
            article.is_publish = True
        else:
            article.is_draft = True
        return article


class ArticlePublish(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['is_publish', 'is_draft']
    
    def save(self, commit=True):
        article = super().save(commit=commit)
        return article
        

class ArticleCommentForm(forms.ModelForm):
    images = forms.FileField(label='Изображения cтатьи', required=False,
                             widget=forms.ClearableFileInput(attrs={"allow_multiple_selected": True}))
    article_id = forms.IntegerField(widget=forms.HiddenInput)
    parent = forms.IntegerField(widget=forms.HiddenInput, required=False)
    
    def save(self, commit=True):
        comment = super().save(commit=commit)
        return comment
    
    def check_exist(self, user):
        parent = self.cleaned_data.get('parent', None)
        if parent:
            comment_exist = ArticleComment.objects.filter(
                author__profile__user=user,
                pk=int(parent),
            ).first()
            return comment_exist
        
    class Meta:
        model = ArticleComment
        fields = ['text', ]
        labels = {
            'text': 'Текст',
        }


class ArticleComplaintForm(forms.ModelForm):
    TITLE = [
        ('1', 'Хамство/грубость'),
        ('2', 'Флуд'),
        ('3', 'Нарушение УК РФ'),
        ('4', 'Реклама'),
        ('5', 'Технические проблемы'),
    ]
    title = forms.ChoiceField(
        choices=TITLE,
        widget=forms.Select(attrs={'class': 'input--select'}),
    )
    object_id = forms.IntegerField(widget=forms.HiddenInput, required=False)
    object_type = forms.ChoiceField(
        choices=[
            ('1', ArticleComment),
            ('2', OverviewComment),
            ('3', CommentConversation),
        ],
        widget=forms.Select(attrs={'type': 'hidden'}),
    )

    class Meta:
        model = Complaint
        fields = ['text', 'title']

        labels = {
            'title': 'Тема жалобы',
            'text': 'Причина жалобы',
        }


class CommentForm(forms.Form):
    object_type = forms.ChoiceField(
        choices=[
            ('1', ArticleComment),
            ('2', OverviewComment),
            ('3', CommentConversation),
        ]
    )
    objects_id = forms.CheckboxSelectMultiple()
