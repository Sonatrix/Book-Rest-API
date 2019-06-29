from rest_framework import status
from rest_framework.test import APIClient, APITestCase


class BookTestCase(APITestCase):
    client = APIClient()
    host = 'http://localhost:8000'

    def test_list_book(self):
        url = self.host+'/api/v1/books'
        response = self.client.get(url, format='json')
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(len(response.data.get("data", [])), 0)
    
    def test_external_api_zero_record(self):
        url = self.host+'/api/external-books?name=a'
        response = self.client.get(url, format='json')
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(len(response.get("data", [])), 0)

    def test_external_api_with_data(self):
        url = f"{self.host}/api/external-books?name=A%20Game%20of%20Thrones"
        response = self.client.get(url, format='json').json()
        self.assertEqual(len(response.get("data", [])), 1)
