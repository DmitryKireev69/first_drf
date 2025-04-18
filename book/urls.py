from django.urls import path, include
from .views import books_list, book_detail, BookListView, BookDetailView, BookDetailView1

urlpatterns = [
    path('', books_list, name='books'),
    path('all/', BookListView.as_view()),
    path('<int:pk>/', book_detail, name='book_detail'),
    path('<int:book_id>/apiview/', BookDetailView.as_view()),
    path('<int:book_id>/generic/', BookDetailView1.as_view())
]