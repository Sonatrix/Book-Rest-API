from django.contrib import admin
from book.models import Author, Publisher, Country, Book

# Register models to admin

admin.site.register(Author)
admin.site.register(Publisher)
admin.site.register(Country)
admin.site.register(Book)
