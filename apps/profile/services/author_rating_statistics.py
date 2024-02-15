from django.db.models import When, Case, Sum, IntegerField, Count
from apps.profile.models import OverviewComment, Overview, SubscribeAction, GratitudeAction
from django.http import JsonResponse
from datetime import datetime, timedelta


def filters(period):
    now_date = datetime.now()
    start_date_week = datetime.now() - timedelta(days=7)
    three_months_ago = datetime.now() - timedelta(days=90)

    period_types = {
            'total': {},
            'week': {'created_at__range': (start_date_week, now_date)},
            'month': {'created_at__month': now_date.month},
            'quarter': {'created_at__month__range': (three_months_ago.month, now_date.month)},
            'year': {'created_at__year': now_date.year},
        }
    return period_types.get(period, {})


def calculate_author_rating_period(obj, period):
    period_type = [
        'week',
        'month',
        'quarter',
        'year',
        'total',
        'readers'
    ]

    if period not in period_type:
        return JsonResponse(
            {
                "message": "Such period name not exists!",
                "status": "error"
            }
        )

    profile_reviews = obj.profile.profile_reviews
    author_comments = obj.author_comments
    overviews = obj.overviews
    if obj.type == obj.AuthorType.READER and period == 'readers':
        return {
            'count_reviews': get_statistic_field_data(profile_reviews, period),
            'count_write_overview_comments': get_statistic_field_data(author_comments, period)
        }
    return {
        'count_overview': get_statistic_field_data(overviews, period),
        'count_subscribers': get_subscribe_gratitude_statistic_date(obj, SubscribeAction, period),
        'count_reviews': get_statistic_field_data(profile_reviews, period),
        'count_views': get_statistic_views_data(overviews, period),
        'count_gratitude': get_subscribe_gratitude_statistic_date(obj, GratitudeAction, period),
        'count_favorite_overview': get_favorite_statistic_date(obj, period),
        'count_likes_overview': get_like_statistic_date(obj, period),
        'count_write_overview_comments': get_statistic_field_data(author_comments, period),
        'count_get_overview_comments': get_overview_comments(obj, period)
    }


def get_statistic_field_data(list_obj, period) -> int:
    return list_obj.filter(**filters(period)).count()


def get_statistic_views_data(list_obj, period) -> int:
    return list_obj.filter(**filters(period)).annotate(
        views_count=Count('views')).aggregate(total_views_count=Sum('views_count'))['total_views_count'] or 0


def get_overview_comments(obj, period) -> int:
    return OverviewComment.objects.filter(overview__author=obj, **filters(period)).count()


def get_like_statistic_date(obj, period) -> int:
    result = Overview.objects.filter(author=obj, is_publish=True, **filters(period)).annotate(
        likes_count=Sum(Case(When(like_action__type_action=1, then=1),
                             When(like_action__type_action=0, then=-1),
                             output_field=IntegerField()))
    ).aggregate(total_likes_count=Sum('likes_count'))

    result_like = result['total_likes_count'] or 0

    return result_like


def get_favorite_statistic_date(obj, period) -> int:
    result = Overview.objects.filter(author=obj, is_publish=True, **filters(period)).annotate(
        favorite_count=Sum(Case(When(favorite_action__type_action=1, then=1),
                             When(favorite_action__type_action=0, then=-1),
                             output_field=IntegerField()))
    ).aggregate(total_favorite_count=Sum('favorite_count'))

    result_favorite = result['total_favorite_count'] or 0
    return result_favorite


def get_subscribe_gratitude_statistic_date(obj, model, period) -> int:
    result = model.objects.filter(author=obj, **filters(period)).annotate(
            count=Sum(Case(When(type_action=1, then=1),
                           When(type_action=0, then=-1),
                           output_field=IntegerField()))).aggregate(total_count=Sum('count'))
    if not result['total_count'] or result['total_count'] < 0:
        return 0
    else:
        return result['total_count']