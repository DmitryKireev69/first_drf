from django.urls import path, include
from .views import *
from rest_framework import routers

router = routers.DefaultRouter()
router.register('books', BookListViewSet2)


urlpatterns = [
    path('', include(router.urls)),
    # path('', books_list, name='books'),
    path('all/', BookListView.as_view()),
    path('<int:pk>/', book_detail, name='book_detail'),
    path('<int:book_id>/apiview/', BookDetailView.as_view()),
    path('<int:book_id>/generic/', BookDetailView1.as_view()),
    path('viewset/', BookListViewSet.as_view({'get':'list','post':'create'})),
    path('viewset/<int:book_id>/',
         BookListViewSet1.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}),
         name='book-detail'),
]