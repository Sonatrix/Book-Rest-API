from rest_framework import serializers
from book.models import Book, Author, Publisher, Country

class BookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = ('name', 'authors', 'isbn', 'number_of_pages', 'publisher', 'country', 'released_at')
        depth = 1
    
    def to_representation(self, obj):
        """
           Return the required results based on specific format
        """
        return {
            'id': obj.id,
            'name': obj.name,
            'isbn': obj.isbn,
            'authors': obj.authors.values_list('name', flat=True),
            'number_of_pages': obj.number_of_pages,
            'publisher': obj.publisher.name,
            'country': obj.country.name,
            'release_date': obj.released_at
        }

