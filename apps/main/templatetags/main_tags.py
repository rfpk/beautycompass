from django import template
from django.conf import settings


register = template.Library()


@register.simple_tag
def site_title():
    return settings.SITE_TITLE


@register.simple_tag
def set_var(val=None):
    return val
