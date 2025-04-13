from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import BookSerializer, LoginSerializer
from .models import Book
from book.models import CustomUser

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
            "login": "test",
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