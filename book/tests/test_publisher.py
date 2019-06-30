from django.test import TestCase
from book.models import Publisher

class PublisherTestCase(TestCase):
    def setUp(self):
        Publisher.objects.create(name="Jai Publications")

    def test_string_representation(self):
        publisher = Publisher(name="jai")
        self.assertEqual(str(publisher), publisher.name)
    
    def test_verbose_name_plural(self):
        self.assertEqual(str(Publisher._meta.verbose_name_plural), "publishers")

    def test_publisher_exists(self):
        """Publisher are correctly identified"""
        publisher = Publisher.objects.get(name="Jai Publications")
        self.assertTrue(isinstance(publisher, Publisher))
        self.assertEqual(publisher.__str__(), publisher.name)
        self.assertEqual(publisher.name, 'Jai Publications')