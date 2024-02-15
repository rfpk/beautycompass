from django.db.models import Max


class StatisticViewMixin:
    @property
    def get_view_count(self) -> int:
        return self.views.count()


class StatisticMixin(StatisticViewMixin):

    @property
    def get_like_count(self) -> int:
        # TODO try optimization
        latest_actions = self.like_action.values('profile').annotate(latest=Max('created_at'))
        return self.like_action.filter(created_at__in=latest_actions.values('latest'),
                                       type_action=1).count()

    @property
    def get_favorite_count(self) -> int:
        # TODO try optimization
        latest_actions_favorite = self.favorite_action.values('profile').annotate(latest=Max('created_at'))
        return self.favorite_action.filter(created_at__in=latest_actions_favorite.
                                           values('latest'), type_action=1).count()

    @property
    def get_comment_count(self) -> int:
        return self.comments.filter(is_publish=True).count()

    def status_favorite(self, user):
        self_action = self.favorite_action.filter(profile__user=user).last()
        if self_action:
            return self_action.type_action
        return False

    def status_likes(self, user):
        self_action = self.like_action.filter(profile__user=user).last()
        if self_action:
            return self_action.type_action
        return False