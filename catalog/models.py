import uuid

from django.db import models

from django.db.models import UniqueConstraint
from django.db.models.functions import Lower
from django.urls import reverse
# Create your models here.


class Genre(models.Model):
    """ Model representing a book genre. """
    name = models.CharField(
        max_length=200,
        unique=True,
        help_text="Enter a book genre (e.g. Science Fiction, French Poetry etc.)"        
    )
    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """Returns the URL to access a particular genre instance."""
        return reverse('genre-detail', args=[str(self.id)])

    class Meta:
        constraints = [
            UniqueConstraint(
                Lower('name'),
                name='genre_name_case_insensitive_unique',
                violation_error_message="Genre already exists (case insensitive match)"
            ),
        ]

class Language(models.Model):
    
    name = models.CharField(
        max_length=200,
        unique=True,
        help_text="Enter the book's natural language (e.g.English, French, Japanese etc.)"
    )

    class Meta:
        constraints = [
            UniqueConstraint(
                Lower('name'),
                name='language_name_case_insensitive_unique',
                violation_error_message="Language already exists (case insensitive match)"
            )
        ]

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("language-detail", args=[str(self.id)])
    


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(
        'Author', 
        on_delete=models.RESTRICT, 
        null=True
    )
    summary = models.TextField(
        max_length=1000,
        help_text="Enter a brief description of the book"
    )
    isbn = models.CharField('ISBN', max_length=13, unique=True, help_text='13 Character <a href="https://www.isbn-insternational.org/content/what-isbn">ISBN</a>')
    # genre = models.ForeignKey('Genre', on_delete=models.CASCADE)
    genre = models.ManyToManyField('Genre', help_text='Select a genre for this book')
    Language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['title', 'author']

    def display_genre(self):
        return ', '.join([genre.name for genre in self.genre.all()[:3]])

    display_genre.short_description = 'Genre'

    def __str__(self):
        return f'{self.title}'
        # return self.title
    
    def get_absolute_url(self):
        """ Returns the URL to access a detail record fo this book. """
        # return reverse("book_detail", kwargs={"pk": self.pk})
        return reverse('book-detail', args=[str(self.id)])

    
class Country(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=3, unique=True, help_text='ISO 3166-1 alpha-3 country code')

    def __str__(self):
        return self.name


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True, help_text='Select the country of the author')
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField(null=True, blank=True)
 
    class Meta:
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f'{self.last_name}. {self.first_name}'

    def get_absolute_url(self):
        return reverse("author_detail", args=[str(self.id)])
    
    

class BookInstance(models.Model):
    """ Model representing a specific copy of a book (i.e. that can be borrowed form the library). """
    id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        help_text="Unique ID for this particular book"
    )
    book = models.ForeignKey('Book', on_delete=models.RESTRICT, null=True)
    imprint = models.CharField(max_length=200)
    
    due_back = models.DateField(null=True, blank=True)
    # borrower = 

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        default='m',
        blank=True,
        help_text='Book availability',
    )

    class Meta:
        ordering = ['due_back']

    def display_author(self):
        return f'{self.book.author.first_name} {self.book.author.last_name}' 

    display_author.short_description = "Author"

    def __str__(self):
        """ String for representing the Model object. """
        return self.book.title


# class MyModelName(models.Model):
#     """A typical class defining a model, derived from the Model class."""

#     # Fields
#     my_field_name = models.CharField(max_length=20, help_text='Enter field documentation')
#     # …

#     # Metadata
#     class Meta:
#         ordering = ['-my_field_name']

#     # Methods
#     def get_absolute_url(self):
#         """Returns the URL to access a particular instance of MyModelName."""
#         return reverse('model-detail-view', args=[str(self.id)])

#     def __str__(self):
#         """String for representing the MyModelName object (in Admin site etc.)."""
#         return self.my_field_name
