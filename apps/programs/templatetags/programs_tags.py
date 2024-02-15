from django import template

register = template.Library()


@register.filter
def ending_word(word):
    return word[:-2] + 'ой' if word else 'Любой'
