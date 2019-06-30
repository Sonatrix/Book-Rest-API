from django.test import TestCase
from book.models import Country, Author, Publisher, Book

class TestCase(TestCase):
    def setUp(self):
        publisher = Publisher.objects.create(name="Jai Publications")
        country = Country.objects.create(name="America")
        author = Author.objects.create(name="Rajesh Mandal")
        book = Book.objects.create(
                name = "Zeshashop",
                isbn = "123-123456123",
                number_of_pages = 100,
                publisher = publisher,
                country = country,
                release_date = "2019-06-02"
            )
        book.authors.set([author])

    def test_country_exists(self):
        """Country are correctly identified"""
        country = Country.objects.get(name="America")
        self.assertEqual(country.name, 'America')
    
    def test_author_exists(self):
        """Author are correctly identified"""
        author = Author.objects.get(name="Rajesh Mandal")
        self.assertEqual(author.name, 'Rajesh Mandal')
    
    def test_publisher_exists(self):
        """Publisher are correctly identified"""
        publisher = Publisher.objects.get(name="Jai Publications")
        self.assertEqual(publisher.name, 'Jai Publications')
    
    def test_create_book(self):
        """Book Creation are successfully done"""
        instance = Book.objects.get(name="Zeshashop")

        
        self.assertEqual(instance.isbn, '123-123456123')
