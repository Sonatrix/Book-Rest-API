import requests
import time
from datetime import datetime
from rest_framework import status, views, filters
from rest_framework.response import Response
from django.http import JsonResponse, Http404
from book.models import Book
from book.serializers import BookSerializer
from book.filters import BookFilter

MAX_RETRIES = 5  # Arbitrary number of times we want to try

# Book List define the view behavior.
class BookListView(views.APIView):
    
    def get(self, request):
        filter_backends = (filters.SearchFilter,)
        queryset = Book.objects.all()
        results = BookFilter(request.GET, queryset=queryset).queryset
        serializer = BookSerializer(results, many=True)
        response = {
            'data': serializer.data,
            'status': 'success',
            'status_code': status.HTTP_200_OK
        }
        return Response(response, status=status.HTTP_200_OK)
    
    def post(self, request):

        serializer = BookSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            response = {
                'data': [{'book': serializer.data}],
                'status': 'success',
                'status_code': status.HTTP_201_CREATED
            }
            return Response(response, status=status.HTTP_201_CREATED)
        return Response({'status': 'failed', 'status_code': 400, 'status': 'failed', 'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

# ViewSets define the view behavior.
class BookView(views.APIView):
    """
    Retrieve, update or delete a snippet instance.
    """

    def get_object(self, id):
        try:
            return Book.objects.get(pk=id)
        except Book.DoesNotExist:
            raise Http404

    def get(self, request, id):
        try:
            queryset = self.get_object(id)
            serializer = BookSerializer([queryset], many=True).data
            response = {
                'data': serializer[0] if len(serializer)>0 else {},
                'status': 'success',
                'status_code': status.HTTP_200_OK
            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as ex:
             return Response({'status': 'failed', 'status_code': 204, 'status': 'failed', 'message': 'No Record found'}, status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, id):
        """
           Update Book Details
        """
        try:
            book = self.get_object(id)
            serializer = BookSerializer(book, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                response = {
                    'data': serializer.data,
                    'status': 'success',
                    'status_code': status.HTTP_200_OK,
                    'message': f'The Book {book.name} was updated successfully'
                }
                return Response(response, status=status.HTTP_200_OK)
            else:
                return Response({'status': 'failed', 'status_code': 400, 'status': 'failed', 'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            return Response({'status': 'failed', 'status_code': 400, 'status': 'failed', 'message': 'Resource does not exist or not found'}, status=status.HTTP_400_BAD_REQUEST)

    
    def delete(self, request, id):
        """
           Method for deleting book with book id passed as param
        """
        try:
            book = self.get_object(id)
            book_name = book.name
            book.delete()
            response_to_send = {
                'data': [],
                'status': 'success',
                'message': f'The book {book_name} was deleted successfully',
                'status_code': status.HTTP_200_OK
            }
            return Response(response_to_send, status=status.HTTP_200_OK)
        except Exception as ex:
            return Response({'status': 'failed', 'status_code': 400, 'status': 'failed', 'message': 'Resource does not exist or not found'}, status=status.HTTP_400_BAD_REQUEST)


# API for Delete and Update.
class BookViewOperation(views.APIView):
    """
        API For update and delete using post method
    """
    def get_object(self, id):
        try:
            return Book.objects.get(pk=id)
        except Book.DoesNotExist:
            raise Http404
    
    def post(self, request, id, action):
        """
           Method for deleting book with book id passed as param based on action
        """
        try:
            book = self.get_object(id)
            book_name = book.name
            response_to_send = {
                'status': 'success',
                'status_code': status.HTTP_200_OK
            }

            if action == "delete":
                book.delete()
                response_to_send.update({
                    'data': [],
                    'message': f'The book {book_name} was deleted successfully'
                })
                return Response(response_to_send, status=status.HTTP_200_OK)
            
            elif action == "update":
                serializer = BookSerializer(book, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    response_to_send.update({
                        'data': serializer.data,
                        'message': f'The Book {book_name} was updated successfully'
                    })

                    return Response(response_to_send, status=status.HTTP_200_OK)
                else:
                    return Response({'status': 'failed', 'status_code': 400, 'status': 'failed', 'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'status': 'failed', 'status_code': 400, 'status': 'failed', 'message': 'Invalid Action'}, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as ex:
            return Response({'status': 'failed', 'status_code': 400, 'status': 'failed', 'message': 'Resource does not exist or not found'}, status=status.HTTP_400_BAD_REQUEST)

    

def external_api_view(request):
    """
       Fetch External Books
    """
    if request.method == "GET":
        params = {}
        
        if request.GET.get('name') is not None:
            params['name'] = request.GET.get('name')

        res = requests.get("https://www.anapioficeandfire.com/api/books", params=params, timeout=10)
        
        if res.status_code == 200:
            data = res.json()
            filtered_res = [{
                'name': obj.get("name", None),
                'isbn': obj.get("isbn", None),
                'authors': obj.get('authors', None),
                'number_of_pages': obj.get("numberOfPages", None),
                'publisher': obj.get("publisher", None),
                'country': obj.get('country', None),
                'released_date': datetime.strptime(obj.get("released", None),"%Y-%m-%dT%H:%M:%S").strftime("%Y-%m-%d")
            } for obj in data]

            response_to_send = {
                'data': filtered_res,
                'status': 'success',
                'status_code': status.HTTP_200_OK
            }

            return JsonResponse(response_to_send, status=status.HTTP_200_OK, safe=False)
        
        return JsonResponse({"message": "Request failed", "status_code": res.status_code, 'status': 'failed'}, status=res.status_code, safe=False)

    return JsonResponse({"message": "Method not allowed", "status_code": status.HTTP_400_BAD_REQUEST, 'status': 'failed'}, status=status.HTTP_400_BAD_REQUEST)
