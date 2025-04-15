from django.contrib.auth import get_user_model
from rest_framework import serializers

from book.models import Book


class One_To_Five:
    """Валидатор на основе класса"""
    def __init__(self, min_value, max_value):
        self.min_value = min_value
        self.max_value = max_value

    def __call__(self, value):
        if not self.min_value <= value <= self.max_value:
            message = f'This field must be a between {self.min_value} and {self.max_value}.'
            raise serializers.ValidationError(message)


def one_to_five(value):
    """Валидатор"""
    if not 0 <= value <= 5:
        raise serializers.ValidationError('Рейтинг должен быть от 0 до 5')


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'


class BookSerializer1(serializers.Serializer):
    title = serializers.CharField(max_length=200, default='Django REST Framework')
    author = serializers.CharField(max_length=100, default='kir')
    ratings = serializers.IntegerField(validators=[one_to_five])
    ratings1 = serializers.IntegerField(validators=[One_To_Five(0, 5)])

    def create(self, validated_data):
        return Book.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.author = validated_data.get('author', instance.author)
        instance.save()
        return instance

    def validate_title(self, value):
        """Валидация на уровне поля"""
        if '1' in value:
            raise serializers.ValidationError('В title не может быть цыфры 1')
        return value

    def validate(self, data):
        """Валидация на уровне обьекта"""
        if data['title'] == data['author']:
            raise serializers.ValidationError("Введены одинаковые значения полей")
        return data


class LoginSerializer(serializers.Serializer):
    login = serializers.CharField()
    password = serializers.CharField(write_only=True)


User = get_user_model()


class CustomUserSerializer(serializers.ModelSerializer):
    # Как пример что можно определить поля и через source связать его
    # author_username = serializers.SerializerMethodField(source='author.username')

    # так же можно создать функцию с get
    # def get_author_username(self, obj):
    #     return obj.author.username

    class Meta:
        model = User
        fields = ('id', 'login', 'name', 'password')
        # Можно использовать или так
        read_only_fields = ('password',)
        # Или так
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user