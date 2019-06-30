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
    
    def test_external_api_with_data(self):
        url = f"{self.host}/api/external-books?name=A%20Game%20of%20Thrones"
        response = self.client.post(url, format='json')
        self.assertTrue(status.is_client_error(response.status_code))

    def test_create_book(self):
        url = self.host+'/api/v1/books'

        payload = {
            "name": "Data",
            "isbn": "1231300138",
            "authors":[{"name": "anjan"}],
            "number_of_pages": 1234,
            "publisher":{"name": "Rajan Publishers"},
            "country": {"name": "UK"},
            "release_date": "2019-06-03"
        }

        response = self.client.post(url, payload, format='json').json()
        self.assertTrue(status.is_success(response["status_code"]))
        self.assertEqual(len(response.get("data")), 1)
    
    def test_create_book_invalid_data(self):
        url = self.host+'/api/v1/books'

        payload = {
            "name": "Data",
            "isbn": "12313001385678",
            "authors":None,
            "number_of_pages": 1234,
            "publisher":{"name": "Rajan Publishers"},
            "country": {"name": "UK"},
            "release_date": "2019-06-03"
        }

        response = self.client.post(url, payload, format='json')
        self.assertTrue(status.is_client_error(response.status_code))

    def test_get_book_details(self):
        url = self.host+'/api/v1/books/2'
        response = self.client.get(url, format='json')
        self.assertTrue(status.is_success(response.status_code))
    
    def test_book_delete_error(self):
        url = self.host+'/api/v1/books/100'
        response = self.client.delete(url, format='json')
        self.assertTrue(status.is_client_error(response.status_code))
    
    def test_book_delete_error_post(self):
        url = self.host+'/api/v1/books/23/delete'
        response = self.client.post(url, {}, format='json')
        self.assertTrue(status.is_client_error(response.status_code))
    
    def test_book_no_action_error_post(self):
        url = self.host+'/api/v1/books/2/action'
        response = self.client.post(url, format='json')
        self.assertTrue(status.is_client_error(response.status_code))
    
    def test_book_update_error_post(self):
        url = self.host+'/api/v1/books/23/update'
        payload = {
            "name": "Java",
            "isbn": "123137777777777700138",
            "authors":[{"name": "Ranjan"}],
            "number_of_pages": 12364,
            "publisher":{"name": "Raju Publishers"},
            "country": {"name": "UKS"},
            "release_date": "2019-06-036"
        }
        response = self.client.post(url, payload, format='json')
        self.assertTrue(status.is_client_error(response.status_code))
    
    def test_filter_book_by_name(self):
        url = self.host+'/api/v1/books?name=Data'
        response = self.client.get(url, format='json').json()
        self.assertEqual(len(response.get("data", [])), 0)
    
    def test_filter_book_by_country(self):
        url = self.host+'/api/v1/books?country=India'
        response = self.client.get(url, format='json').json()
        self.assertEqual(len(response.get("data", [])), 0)
    
    def test_filter_book_by_publisher(self):
        url = self.host+'/api/v1/books?publisher=Data'
        response = self.client.get(url, format='json').json()
        self.assertEqual(len(response.get("data", [])), 0)
    
    def test_filter_book_by_release_date(self):
        url = self.host+'/api/v1/books?release_date=2019'
        response = self.client.get(url, format='json').json()
        self.assertEqual(len(response.get("data", [])), 0)
    
    def test_update_book_data(self):
        url = self.host+'/api/v1/books/1'

        payload = {
            "name": "Java",
            "isbn": "1231300138",
            "authors":[{"name": "Ranjan"}],
            "number_of_pages": 12364,
            "publisher":{"name": "Raju Publishers"},
            "country": {"name": "UKS"},
            "release_date": "2019-06-03"
        }

        response = self.client.patch(url, payload, format='json')
        self.assertTrue(status.is_client_error(response.status_code))
    
    def test_book_get_data(self):
        """ Create book and get it by response"""
        url = self.host+'/api/v1/books'

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
            get_url = self.host+'/api/v1/books/'+str(response['data'][0]['book']['id'])
            res = self.client.get(get_url)
            self.assertTrue(status.is_success(res.status_code))
        else:
            pass
    
    def test_book_update_data(self):
        """ Create book and update it by response"""
        url = self.host+'/api/v1/books'

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
            get_url = self.host+'/api/v1/books/'+str(response['data'][0]['book']['id'])
            res = self.client.patch(get_url, payload, format='json')
            self.assertTrue(status.is_success(res.status_code))
        else:
            pass
    
    def test_book_delete_bad_request(self):
        """ Create book and delete it by id"""
        url = self.host+'/api/v1/books'

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
            get_url = self.host+'/api/v1/books/'+str(response['data'][0]['book']['id'])
            res = self.client.delete(get_url, format='json')
            self.assertTrue(status.is_success(res.status_code))
        else:
            pass
        
    def test_book_update_bad_request(self):
        """ Create book and update it by id Error"""
        url = self.host+'/api/v1/books'

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
            get_url = self.host+'/api/v1/books/'+str(response['data'][0]['book']['id'])
            payload = payload.update({"ssn": "3235236347485795696797"})
            res = self.client.patch(get_url, payload, format='json')
            self.assertTrue(status.is_client_error(res.status_code))
        else:
            pass
        

    def test_book_post_delete_bad_request(self):
        """ Create book and delete it by id"""
        url = self.host+'/api/v1/books'

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
            get_url = self.host+'/api/v1/books/'+str(response['data'][0]['book']['id'])+'/delete'
            res = self.client.post(get_url, format='json')
            self.assertTrue(status.is_success(res.status_code))
        else:
            pass
    
    def test_book_post_delete_bad_request(self):
        """ Create post book and delete it by id"""
        url = self.host+'/api/v1/books'

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
            get_url = self.host+'/api/v1/books/'+str(response['data'][0]['book']['id'])+'/patch'
            res = self.client.post(get_url, payload, format='json')
            self.assertTrue(status.is_client_error(res.status_code))
        else:
            pass
    
    def test_book_post_update_success_request(self):
        """ Create post book and update it by id"""
        url = self.host+'/api/v1/books'

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
            get_url = self.host+'/api/v1/books/'+str(response['data'][0]['book']['id'])+'/update'
            res = self.client.post(get_url, payload, format='json')
            self.assertTrue(status.is_success(res.status_code))
        else:
            pass
        




        



