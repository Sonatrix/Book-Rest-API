from django.urls import path, include
from rest_framework import routers
from book.views import BookViewSet, external_api_view

app_name = 'book'

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'books', BookViewSet, basename='book')

urlpatterns = [
    path('external-books', external_api_view, name='external-books'),
    path('v1/', include(router.urls), name='book'),
]
