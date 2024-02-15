from rest_framework import serializers
from apps.blog.models import Article

class ManufacturerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Article
        fields = ['id', 'title', 'thumbnail', 'date', 'text', 'slug']
