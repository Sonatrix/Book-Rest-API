from django.urls import path, include
from rest_framework import routers
from book.views import BookListView, BookView, external_api_view

app_name = 'book'

urlpatterns = [
    path('external-books', external_api_view, name='external-books'),
    path('v1/books', BookListView.as_view(), name='book-list'),
    path('v1/books/<int:id>', BookView.as_view(), name='book-detail'),
]
