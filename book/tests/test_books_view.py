from django.urls import reverse
from rest_framework import status
from django.test import TestCase, Client
from book.models import Country, Author, Publisher, Book
from book.serializers import BookSerializer

class BooksAPITestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.publisher = Publisher.objects.create(name="Jai Publications")
        self.country = Country.objects.create(name="America")
        self.author = Author.objects.create(name="Rajesh Mandal")
        self.book = Book.objects.create(
                name = "Zeshashop",
                isbn = "123-12345612",
                number_of_pages = 100,
                publisher = self.publisher,
                country = self.country,
                release_date = "2019-06-02"
            )
        self.book.authors.set([self.author])

    def tearDown(self):
        del self.client
    

    def test_list_books(self):
        # get API response
        response = self.client.get(reverse('book:books-view'))
        # get data from db
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        self.assertEqual(len(response.json().get('data')), len(serializer.data))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_list_books_bad_request(self):
        # get API response
        response = self.client.put(reverse('book:books-view'))
        self.assertTrue(status.is_client_error(response.status_code))
