from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import BookSerializer, LoginSerializer
from .models import Book
from book.models import CustomUser
from rest_framework.decorators import api_view
from django.http import Http404
from rest_framework.generics import GenericAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin

class BookListView2(ListCreateAPIView):
    """Переделали на основе готового мексина для get и post запросов"""
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookListView1(GenericAPIView, ListModelMixin, CreateModelMixin):
    """Представление на основе миксинов List и Create"""
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class BookDetailView2(RetrieveUpdateDestroyAPIView):
    """Переделали на основе готового миксина"""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'book_id'

class BookDetailView1(GenericAPIView, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin):
    """Представление на основе миксинов для 1 обьекта ретрив обновление и удаление"""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    # Определяет поле модели, по которому будет искаться объект.
    lookup_field = 'id'
    # Использует 'book_id' из URL по умолчанию используется то же значение, что и lookup_field
    lookup_url_kwarg = 'book_id'

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class BookDetailView(APIView):

    def get_object(self, pk):
        book = Book.objects.filter(pk=pk).first()
        if not book:
            raise Http404
        return book

    def get(self, request, *args, **kwargs):
        book = self.get_object(kwargs.get('book_id'))
        serializer = BookSerializer(book)
        return Response(serializer.data, status=200)

    def put(self, request, *args, **kwargs):
        book = self.get_object(kwargs.get('book_id'))
        serializer = BookSerializer(book, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=200)

    def patch(self, request, *args, **kwargs):
        book = self.get_object(kwargs.get('book_id'))
        serializer = BookSerializer(book, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=200)

    def delete(self, request, *args, **kwargs):
        book = self.get_object(kwargs.get('book_id'))
        book.delete()
        return Response(status=204)


class BookListView(APIView):

    def get(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data, status=200)

    def post(self, request):
        data = request.data
        serializer = BookSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)


@api_view(['GET', 'POST'])
def books_list(request):
    if request.method == 'GET':
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@api_view(['GET', 'PUT', 'DELETE', 'PATCH'])
def book_detail(request, pk):
    book = Book.objects.filter(pk=pk).first()
    if not book:
        return Response(status=404)

    if request.method == 'GET':
        serializer = BookSerializer(book)
        return Response(serializer.data, status=200)
    elif request.method == 'PUT' or request.method == 'PATCH':
        if request.method == 'PUT':
            serializer = BookSerializer(book, request.data)
        else:
            serializer = BookSerializer(book, request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=200)
    elif request.method == 'DELETE':
        book.delete()
        return Response(status=204)


class TestView(APIView):
    def get(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        serializer = BookSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, book_id):
        book = Book.objects.get(pk=book_id)
        serializer = BookSerializer(book, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, book_id):
        book = Book.objects.get(pk=book_id)
        serializer = BookSerializer(book, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

class LoginView(APIView):

    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        data = {
            "login": "user",
            "password": "100"
        }
        serializer = LoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            # выполняем аунтификацию
            user = authenticate(
                username=serializer.validated_data.get('login'),
                password=serializer.validated_data.get('password')
            )
            if user is None:
                return Response(status=status.HTTP_401_UNAUTHORIZED)

            # выпошлняем авторизацию
            login(request, user)
            return Response(status=status.HTTP_200_OK)


class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)