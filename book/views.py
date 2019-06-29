import requests
import time
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.http import JsonResponse
from book.models import Book, Author
from book.serializers import BookSerializer

MAX_RETRIES = 5  # Arbitrary number of times we want to try

# ViewSets define the view behavior.
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def list(self, request):
        
        serializer = BookSerializer(self.queryset, many=True)
        response = {
            'data': serializer.data,
            'status': 'success',
            'status_code': status.HTTP_200_OK
        }
        return Response(response, status=status.HTTP_200_OK)


def external_api_view(request):
    if request.method == "GET":
        attempt_num = 0  # keep track of how many times we've retried
        params = {}
        params['name'] = request.GET.get('name')

        while attempt_num < MAX_RETRIES:
            r = requests.get("https://www.anapioficeandfire.com/api/books", params=params, timeout=10)
            
            if r.status_code == 200:
                data = r.json()
                filtered_res = [{
                    'name': obj.get("name", None),
                    'isbn': obj.get("isbn", None),
                    'authors': obj.get('authors', None),
                    'number_of_pages': obj.get("numberOfPages", None),
                    'publisher': obj.get("publisher", None),
                    'country': obj.get('country', None),
                    'release_date': obj.get("released", None)
                } for obj in data]

                response_to_send = {
                    'data': filtered_res,
                    'status': 'success',
                    'status_code': status.HTTP_200_OK
                }
                return JsonResponse(response_to_send, status=status.HTTP_200_OK, safe=False)
            else:
                attempt_num += 1
                # You can probably use a logger to log the error here
                time.sleep(5)  # Wait for 5 seconds before re-trying
        
        return JsonResponse({"message": "Request failed", "status_code": r.status_code, 'status': 'failed'}, status=r.status_code, safe=False)
    else:
        return JsonResponse({"message": "Method not allowed", "status_code": r.HTTP_400_BAD_REQUEST, 'status': 'failed'}, status=status.HTTP_400_BAD_REQUEST)
