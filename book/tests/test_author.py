from django.test import TestCase
import nose.tools as nt
from book.models import Author

class AuthorTestCase(TestCase):
    def setUp(self):
        self.author = Author.objects.create(name="Jai Prakash")

    def tearDown(self):
        self.author.delete()

    def test_author_created(self):
        """Authors are  created"""
        self.assertTrue(isinstance(self.author, Author))
        nt.eq_(self.author.__str__(), self.author.name)

    def test_string_representation(self):
        self.assertEqual(str(self.author), self.author.name)
    
    def test_verbose_name_plural(self):
        nt.eq_(str(Author._meta.verbose_name_plural), "authors")
    
    def test_second_publisher_created(self):
        author = Author.objects.create(name="Rajesh")
        self.assertNotEqual(self.author.name, author.name)
        self.assertNotEqual(self.author.id, author.id)
        author.delete()

    