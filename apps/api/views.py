from rest_framework import viewsets
from rest_framework.response import Response

from apps.api.pagination import ManufacturerArticlePagination
from apps.api.serializers import ManufacturerSerializer

from apps.blog.models import Article


class ManufacturerArticlesView(viewsets.ModelViewSet):
    serializer_class = ManufacturerSerializer
    pagination_class = ManufacturerArticlePagination
    http_method_names = ['get', ]

    def get_queryset(self):
        return Article.objects.filter(manufacturer__pk=self.kwargs['pk'])

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        return self.list(self, request, *args, **kwargs)
