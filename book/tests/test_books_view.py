import json
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

        self.valid_payload = {
            "name": "Java",
            "isbn": "12313777138",
            "authors": [{"name": "Ranjan"}],
            "number_of_pages": 12364,
            "publisher": {"name": "Raju Publishers"},
            "country": {"name": "UKS"},
            "release_date": "2019-06-03"
        }

        self.invalid_payload = {
            "name": "Java",
            "isbn": "12313777138",
            "authors": [{"name": "Ranjan"}],
            "number_of_pages": 12364,
            "publisher": {"name": "Raju Publishers"},
            "country": {"name": "UKS"},
            "release_date": "2019-06-034"
        }

    def tearDown(self):
        del self.client
        self.book.delete()
        self.publisher.delete()
        self.author.delete()
        self.country.delete()
    
    def test_list_books(self):
        # get API response
        response = self.client.get(reverse('book:books-view'))
        # get data from db
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        self.assertEqual(len(response.json().get('data')), len(serializer.data))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_list_books_bad_request(self):
        # BAD API response
        response = self.client.put(reverse('book:books-view'))
        self.assertTrue(status.is_client_error(response.status_code))
    
    def test_create_book(self):
        url = reverse('book:books-view')

        response = self.client.post(url, data=json.dumps(self.valid_payload), content_type='application/json').json()
        self.assertTrue(status.is_success(response["status_code"]))
        self.assertEqual(len(response.get("data")), 1)
    
    def test_create_book_invalid_data(self):
        url = reverse('book:books-view')

        response = self.client.post(url, data=json.dumps(self.invalid_payload), content_type='application/json')
        self.assertTrue(status.is_client_error(response.status_code))
    
    def test_filter_book_by_name(self):
        url = reverse('book:books-view')
        response = self.client.get(url, {'name': "Zeshashop"}).json()
        self.assertEqual(len(response.get("data", [])), 1)
    
    def test_filter_book_by_publisher(self):
        url = reverse('book:books-view')
        response = self.client.get(url, {'publisher': "Jai Publications"}).json()
        self.assertEqual(len(response.get("data", [])), 1)
    
    def test_filter_book_by_release_date(self):
        url = reverse('book:books-view')
        response = self.client.get(url, {'release_date': 2019}).json()
        self.assertEqual(len(response.get("data", [])), 1)
    
    def test_filter_book_by_country(self):
        url = reverse('book:books-view')
        response = self.client.get(url, {'country': "America"}).json()
        self.assertEqual(len(response.get("data", [])), 1)
