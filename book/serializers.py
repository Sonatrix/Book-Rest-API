from rest_framework import serializers
from book.models import Book


class BookSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Book
        fields = ('name', 'authors', 'isbn', 'number_of_pages', 'publisher', 'country', 'released_at')
