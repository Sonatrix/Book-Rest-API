from django.test import TestCase
import nose.tools as nt
from book.models import Publisher

class PublisherTestCase(TestCase):
    def setUp(self):
        self.publisher = Publisher.objects.create(name="Jai Publications")

    def tearDown(self):
        self.publisher.delete()

    def test_publisher_created(self):
        """Publisher are correctly identified"""
        self.assertTrue(isinstance(self.publisher, Publisher))
        nt.eq_(self.publisher.__str__(), self.publisher.name)

    def test_string_representation(self):
        self.assertEqual(str(self.publisher), self.publisher.name)
    
    def test_verbose_name_plural(self):
        nt.eq_(str(Publisher._meta.verbose_name_plural), "publishers")
    
    def test_second_publisher_created(self):
        publisher = Publisher.objects.create(name="Hannover")
        self.assertNotEqual(self.publisher.name, publisher.name)
        self.assertNotEqual(self.publisher.id, publisher.id)
        publisher.delete()

    