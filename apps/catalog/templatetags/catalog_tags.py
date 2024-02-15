from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def get_list(dictionary, key):
    return dictionary.getlist(key)


@register.filter
def to_bold(value, word):
    text = value.lower().replace(word.lower(), f'<strong>{word}</strong>')
    text = mark_safe(text)
    return text
