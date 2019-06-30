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
        self.assertTrue(isinstance(country, Country))
        self.assertEqual(country.__str__(), country.name)
        self.assertTrue(isinstance(country.__str__, object))
        self.assertEqual(country.name, "America")
    
    def test_author_exists(self):
        """Author are correctly identified"""
        author = Author.objects.get(name="Rajesh Mandal")
        self.assertTrue(isinstance(author, Author))
        self.assertEqual(author.__str__(), author.name)
        self.assertEqual(author.name, 'Rajesh Mandal')
    
    def test_publisher_exists(self):
        """Publisher are correctly identified"""
        publisher = Publisher.objects.get(name="Jai Publications")
        self.assertTrue(isinstance(publisher, Publisher))
        self.assertEqual(publisher.__str__(), publisher.name)
        self.assertEqual(publisher.name, 'Jai Publications')
    
    def test_create_book(self):
        """Book Creation are successfully done"""
        instance = Book.objects.get(name="Zeshashop")
        self.assertTrue(isinstance(instance, Book))
        self.assertEqual(instance.__str__(), instance.name)
        self.assertEqual(instance.name, 'Zeshashop')
        self.assertEqual(instance.isbn, '123-123456123')
    
    def test_if_book_no_exists(self):
        """Test if book does not exist"""
        instance = Book.objects.filter(id=3).exists()
        
        self.assertEqual(instance, False)
