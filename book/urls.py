from django.urls import path, include
from .views import books_list, book_detail, BookListView, BookDetailView

urlpatterns = [
    path('', books_list, name='books'),
    path('all/', BookListView.as_view()),
    path('<int:pk>/', book_detail, name='book_detail'),
    path('<int:book_id>/base/', BookDetailView.as_view())
]