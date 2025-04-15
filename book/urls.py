from django.urls import path, include
from .views import books_list, book_detail

urlpatterns = [
    path('', books_list, name='books'),
    path('<int:pk>/', book_detail, name='book_detail')
]