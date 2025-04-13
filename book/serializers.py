from django.contrib.auth import get_user_model
from rest_framework import serializers

from book.models import Book


class BookSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200, default='Django REST Framework')
    author = serializers.CharField(max_length=100, default='kir')

    def create(self, validated_data):
        return Book.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.author = validated_data.get('author', instance.author)
        instance.save()
        return instance


class LoginSerializer(serializers.Serializer):
    login = serializers.CharField()
    password = serializers.CharField(write_only=True)


User = get_user_model()


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'login', 'name', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user