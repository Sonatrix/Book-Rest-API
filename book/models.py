from django.db import models

class Author(models.Model):
    """ Model representing book author details """
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Publisher(models.Model):
    """ Model representing publisher detail """
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Country(models.Model):
    """ Model representing country """
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Book(models.Model):
    """Model representing a book."""

    name = models.CharField(max_length=200)

    # ManyToManField Key used because books can have many author (Section Wise), but authors can have multiple books
    authors = models.ManyToManyField(Author, help_text="Select Authors for book")
    
    description = models.TextField(max_length=1000, help_text='Enter a brief description of the book')
    isbn = models.CharField('ISBN', max_length=13, help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>', unique=True)
    
    number_of_pages = models.IntegerField(blank=False, null=False)
    publisher = models.ForeignKey(Publisher, help_text='Select publisher', on_delete=models.SET_NULL, null=True)
    country = models.ForeignKey(Country, help_text='Select Country', on_delete=models.SET_NULL, null=True)
    
    created_at = models.DateField(null=True, blank=True, auto_now=True)
    release_date = models.DateField('Released Date', null=True, blank=True)

    def __str__(self):
        return self.name
