from rest_framework import serializers

from book.models import Book


class BookSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200, default='Django REST Framework')
    author = serializers.CharField(max_length=100, default='kir')

    def create(self, validated_data):
        return Book.objects.create(**validated_data)
