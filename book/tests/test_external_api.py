from django.urls import reverse
from rest_framework import status
from django.test import TestCase, Client

class ExternalAPITestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def tearDown(self):
        del self.client
    
    def test_external_api_zero_record(self):
        url = reverse('book:external-books')
        response = self.client.get(url, {'name': "a"})
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(len(response.get("data", [])), 0)

    def test_external_api_with_data(self):
        url = reverse('book:external-books')
        response = self.client.get(url, {'name': "A Dance with Dragons"}).json()
        self.assertEqual(len(response.get("data", [])), 1)
    
    def test_external_api_bad_request(self):
        url = reverse('book:external-books')
        response = self.client.post(url, {'name': "A Dance with Dragons"})
        self.assertTrue(status.is_client_error(response.status_code))
    