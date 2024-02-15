from django import template

from apps.tools.database_operations import ADD

register = template.Library()


@register.simple_tag
def status_favorite(obj, user):
    self_action = obj.favorite_action.filter(profile__user=user).last()
    if self_action:
        return self_action.type_action
    return False


@register.simple_tag
def status_subscribe_brand(obj, user):
    last_action = obj.brand_subscribers.filter(profile__user=user).last()
    if last_action:
        return last_action.type_action
    return False

