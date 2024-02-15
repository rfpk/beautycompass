from django.db.models import Case, When, IntegerField, Sum, Count
from django.db.models.functions import TruncDay
from django.shortcuts import get_object_or_404
from apps.profile.models import FavoriteAction, LikeAction
from apps.tools.utils import filter_data


def get_reviews_statistic_data(model_name, filter_filed, pk):
    # data of reviews product or comment article
    return list(model_name.objects.filter(**{f'{filter_filed}__pk': pk}).annotate(day=TruncDay('created_at')).
                values('day').annotate(value=Count('id', output_field=IntegerField())).order_by('day').
                values('day', 'value'))


def get_statistic_model_data(model_statistic, model_name, pk):
    # data of View/Conversion/ViewLinks
    return list(model_statistic.objects.filter(content_type__model=model_name, object_id=pk). \
                annotate(day=TruncDay('created_at')).values('day'). \
                annotate(value=Sum(Case(When(type_action=1, then=1)), default=0,
                                   output_field=IntegerField())).order_by('day').values('day', 'value'))


def get_statistic_links_data(model_name, pk) -> list:
    # data of links
    """
    returned data example:
    [
    {'day':datetime.datetime(2023, 8, 25, 0, 0, tzinfo=zoneinfo.ZoneInfo(key='UTC')),
     'WB': 1, 'OZON': 1, 'total_value': 2},

    {'day': datetime.datetime(2023, 8, 26, 0, 0, tzinfo=zoneinfo.ZoneInfo(key='UTC')),
     'WB': 2, 'OZON': 2, 'total_value': 4}
    ]
    """
    obj = get_object_or_404(filter_data[model_name]['model'], pk=pk)
    if obj.__class__.__name__ == 'Brand':
        list_obj = obj.brand_links
    else:
        list_obj = obj.product_links

    data = list(list_obj.annotate(day=TruncDay('link_conversion__created_at')).values('day').annotate(
        **{f'{obj.name}': Sum(
            Case(When(link_conversion__type_action=1, link_conversion__object_id=obj.pk, then=1), default=0,
                 output_field=IntegerField())) for obj in list_obj.all()},
        total_value=Sum(Case(When(link_conversion__type_action=1, then=1), default=0, output_field=IntegerField()
                             ))))
    return data


def get_favorites_statistic_data(model_name, pk):
    # data add/remove from favorites for chart
    return list(FavoriteAction.objects.filter(content_type__model=model_name, object_id=pk). \
                annotate(day=TruncDay('created_at')).values('day').\
                annotate(add_value=Sum(Case(When(type_action=1, then=1)),
                                       default=0, output_field=IntegerField())). \
                annotate(remove_value=Sum(Case(When(type_action=0, then=1)),
                                          default=0, output_field=IntegerField())).order_by('day').
                values('day', 'add_value', 'remove_value'))


def get_likes_statistic_data(model_name, pk):
    # data likes for chart
    from django.db.models import Sum

    likes_by_day = list(LikeAction.objects.filter(content_type__model=model_name, object_id=pk).
                        annotate(day=TruncDay('created_at')).values('day').annotate(
        value=Sum(Case(When(type_action=1, then=1), When(type_action=0, then=-1)), default=0,
                  output_field=IntegerField())).order_by('day'))

    count = 0
    for obj_id, obj in enumerate(likes_by_day):
        count += obj['value']
        likes_by_day[obj_id] = {'day': obj['day'], 'value': count}
    return likes_by_day
