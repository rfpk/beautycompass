from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class ManufacturerArticlePagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page'
    max_page_size = 10

    def get_paginated_response(self, data):
        return Response({
            'total': self.page.paginator.count,
            'page': self.page.number,
            'data': data,
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
        })
