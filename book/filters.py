import django_filters
from book.models import Book

class BookFilter(django_filters.FilterSet):
    class Meta:
        model = Book
        fields = {
            'name': ['exact', 'icontains'],
            'publisher__name': ['exact', 'icontains'],
            'country__name': ['exact', 'icontains'],
            'release_date': ['exact', 'year__gt'],
        }
