from django import template

register = template.Library()


@register.simple_tag
def status_gratitude(obj, user):
    last_action = obj.author_gratitudes.filter(author_action__profile__user=user).last()
    if last_action:
        return last_action.type_action
    return False


@register.simple_tag
def status_subscribe(obj, user):
    last_action = obj.author_subscribers.filter(author_action__profile__user=user).last()
    if last_action:
        return last_action.type_action
    return False


@register.filter
def get_item_by_key(dictionary, key):
    return dictionary.get(key)


@register.simple_tag(takes_context=True)
def get_test(context, name, value):
    return context.get(name + '_' + str(value), None)
