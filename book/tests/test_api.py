import json
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from book.models import Country, Author, Publisher, Book

class BookTestCase(APITestCase):
    client = APIClient()

    def setUp(self):
        self.publisher = Publisher.objects.create(name="Jai Publications")
        self.country = Country.objects.create(name="America")
        self.author = Author.objects.create(name="Rajesh Mandal")
        self.book = Book.objects.create(
                name = "Zeshashop",
                isbn = "123-123456123",
                number_of_pages = 100,
                publisher = self.publisher,
                country = self.country,
                release_date = "2019-06-02"
            )
        self.book.authors.set([self.author])

        self.invalid_payload = {
            "name": "Java",
            "isbn": "123137777777777700138",
            "authors":[{"name": "Ranjan"}],
            "number_of_pages": 12364,
            "publisher":{"name": "Raju Publishers"},
            "country": {"name": "UKS"},
            "release_date": "2019-06-036"
        }

        self.valid_payload = {
            "name": "Java",
            "isbn": "1231300138",
            "authors":[{"name": "Ranjan"}],
            "number_of_pages": 12364,
            "publisher":{"name": "Raju Publishers"},
            "country": "UKS",
            "release_date": "2019-06-03"
        }

    def tearDown(self):
        self.book.delete()
        self.publisher.delete()
        self.author.delete()
        self.country.delete()

    def test_get_book_detail_by_id(self):
        "Test Book Details By ID"
        url = reverse('book:book-view', kwargs={'id': 2})
        response = self.client.get(url, format='json')
        self.assertTrue(status.is_success(response.status_code))
    
    def test_book_delete_error(self):
        url = reverse('book:book-view', kwargs={'id': 100})
        response = self.client.delete(url, format='json')
        self.assertTrue(status.is_client_error(response.status_code))
    
    def test_book_delete_error_post(self):
        url = reverse('book:book-actions', kwargs={'id': 100, 'action': 'delete'})
        response = self.client.post(url, {}, format='json')
        self.assertTrue(status.is_client_error(response.status_code))
    
    def test_book_no_action_error_post(self):
        url = reverse('book:book-actions', kwargs={'id': 2, 'action': 'invalid'})
        response = self.client.post(url, format='json')
        self.assertTrue(status.is_client_error(response.status_code))
    
    def test_book_update_error_post(self):
        url = reverse('book:book-actions', kwargs={'id': 23, 'action': 'update'})
        
        response = self.client.post(url, self.invalid_payload, format='json')
        self.assertTrue(status.is_client_error(response.status_code))
    
    def test_update_book_data(self):
        url = reverse('book:book-view', kwargs={'id': 1})
        response = self.client.patch(url, self.valid_payload, format='json')
        self.assertTrue(status.is_client_error(response.status_code))
    
    def test_book_get_data(self):
        """ Create book and get it by response"""
        url = '/api/v1/books'

        payload = {
            "name": "Java",
            "isbn": "1231300138",
            "authors":[{"name": "Ranjan"}],
            "number_of_pages": 12364,
            "publisher":{"name": "Raju Publishers"},
            "country": {"name": "UKS"},
            "release_date": "2019-06-03"
        }

        response = self.client.post(url, payload, format='json').json()
        if response.get('status_code') == 201:
            print(response)
            get_url = '/api/v1/books/'+str(response['data'][0]['book']['id'])
            res = self.client.get(get_url)
            self.assertTrue(status.is_success(res.status_code))
        else:
            pass
    
    def test_book_update_data(self):
        """ Create book and update it by response"""
        url = '/api/v1/books'

        payload = {
            "name": "Java",
            "isbn": "1230138",
            "authors":[{"name": "Ranjan"}],
            "number_of_pages": 12364,
            "publisher":{"name": "Raju Publishers"},
            "country": {"name": "UKS"},
            "release_date": "2019-06-03"
        }

        response = self.client.post(url, payload, format='json').json()
        if response.get('status_code') == 201:
            get_url = '/api/v1/books/'+str(response['data'][0]['book']['id'])
            res = self.client.patch(get_url, payload, format='json')
            self.assertTrue(status.is_success(res.status_code))
        else:
            pass
    
    def test_book_delete_bad_request(self):
        """ Create book and delete it by id"""
        url = '/api/v1/books'

        payload = {
            "name": "Python",
            "isbn": "100000",
            "authors":[{"name": "Ranjan"}],
            "number_of_pages": 12364,
            "publisher":{"name": "Raju Publishers"},
            "country": {"name": "UKS"},
            "release_date": "2013-06-03"
        }

        response = self.client.post(url, payload, format='json').json()

        if response.get('status_code') == 201:
            get_url = '/api/v1/books/'+str(response['data'][0]['book']['id'])
            res = self.client.delete(get_url, format='json')
            self.assertTrue(status.is_success(res.status_code))
        else:
            pass
        
    def test_book_update_bad_request(self):
        """ Create book and update it by id Error"""
        url = '/api/v1/books'

        payload = {
            "name": "Java",
            "isbn": "100138",
            "authors":[{"name": "Ranjan"}],
            "number_of_pages": 12364,
            "publisher":{"name": "Raju Publishers"},
            "country": {"name": "UKS"},
            "release_date": "2019-06-03"
        }

        response = self.client.post(url, payload, format='json').json()

        if response.get('status_code') == 201:
            get_url = '/api/v1/books/'+str(response['data'][0]['book']['id'])
            payload = payload.update({"ssn": "3235236347485795696797"})
            res = self.client.patch(get_url, payload, format='json')
            self.assertTrue(status.is_client_error(res.status_code))
        else:
            pass
        

    def test_book_post_delete_bad_request(self):
        """ Create book and delete it by id"""
        url = '/api/v1/books'

        payload = {
            "name": "Python",
            "isbn": "100000",
            "authors":[{"name": "Ranjan"}],
            "number_of_pages": 12364,
            "publisher":{"name": "Raju Publishers"},
            "country": {"name": "UKS"},
            "release_date": "2013-06-03"
        }

        response = self.client.post(url, payload, format='json').json()

        if response.get('status_code') == 201:
            get_url = '/api/v1/books/'+str(response['data'][0]['book']['id'])+'/delete'
            res = self.client.post(get_url, format='json')
            self.assertTrue(status.is_success(res.status_code))
        else:
            pass
    
    def test_book_post_delete_bad_request(self):
        """ Create post book and delete it by id"""
        url = '/api/v1/books'

        payload = {
            "name": "Python",
            "isbn": "100000",
            "authors":[{"name": "Ranjan"}],
            "number_of_pages": 12364,
            "publisher":{"name": "Raju Publishers"},
            "country": {"name": "UKS"},
            "release_date": "2013-06-03"
        }

        response = self.client.post(url, payload, format='json').json()

        if response.get('status_code') == 201:
            get_url = '/api/v1/books/'+str(response['data'][0]['book']['id'])+'/patch'
            res = self.client.post(get_url, payload, format='json')
            self.assertTrue(status.is_client_error(res.status_code))
        else:
            pass
    
    def test_book_post_update_success_request(self):
        """ Create post book and update it by id"""
        url = '/api/v1/books'

        payload = {
            "name": "Python",
            "isbn": "100000",
            "authors":[{"name": "Ranjan"}],
            "number_of_pages": 12364,
            "publisher":{"name": "Raju Publishers"},
            "country": {"name": "UKS"},
            "release_date": "2013-06-03"
        }

        response = self.client.post(url, payload, format='json').json()

        if response.get('status_code') == 201:
            get_url = '/api/v1/books/'+str(response['data'][0]['book']['id'])+'/update'
            res = self.client.post(get_url, payload, format='json')
            self.assertTrue(status.is_success(res.status_code))
        else:
            pass
        




        



