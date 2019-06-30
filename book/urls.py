from django.urls import path, include
from rest_framework import routers
from book.views import BookListView, BookView, BookViewOperation, external_api_view

app_name = 'book'

urlpatterns = [
    path('external-books', external_api_view, name='external-books'),
    path('v1/books', BookListView.as_view(), name='books-view'),
    path('v1/books/<int:id>', BookView.as_view(), name='book-view'),
    path('v1/books/<int:id>/<action>', BookViewOperation.as_view(), name='book-actions'),
]
