from rest_framework import serializers
from book.models import Book, Author, Publisher, Country

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'

class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = '__all__'

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'
    
class BookSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True)
    publisher = PublisherSerializer()
    country = CountrySerializer()

    class Meta:
        model = Book
        fields = ('name', 'authors', 'isbn', 'number_of_pages', 'publisher', 'country', 'release_date')
        depth = 1
    
    def to_representation(self, obj):
        """
           Return the required results based on specific format
        """
        return {
            'id': obj.id,
            'name': obj.name,
            'isbn': obj.isbn,
            'authors': obj.authors.values_list('name', flat=True) if obj.authors is not None else [],
            'number_of_pages': obj.number_of_pages,
            'publisher': obj.publisher.name if obj.publisher is not None else None,
            'country': obj.country.name if obj.country is not None else None,
            'release_date': obj.release_date
        }
    
    def create(self, validated_data):
        authors = validated_data.pop('authors')
        publisher = validated_data.pop('publisher')
        country = validated_data.pop('country')

        book = Book.objects.create(**validated_data)

        # Create publisher if not exists
        publish_obj, created = Publisher.objects.get_or_create(name=publisher.get('name'))
        book.publisher = publish_obj
        
        # add country if not exists
        country_obj, created = Country.objects.get_or_create(name=country.get('name'))
        book.country = country_obj
        
        # Add authors for book
        for author in authors:
            author_obj, created = Author.objects.get_or_create(name=author['name'])
            book.authors.add(author_obj)
        
        # save the data for nested author, country and publisher
        book.save()

        return book
