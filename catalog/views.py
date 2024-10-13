from django.shortcuts import render
from django.http import HttpResponse
from .models import Book, Author, BookInstance, Genre, Country

# Create your views here.

def index(request):
    # return HttpResponse("This is the context from catalog index.")
    # Generate counts of some of the main objects.
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # The 'all()' is implied by default.
    num_authors = Author.objects.count()

    # Genre count
    num_genre = Genre.objects.count()

    # Books which title contains the, case insensitive
    filter_word = 'the'
    num_books_filtered = Book.objects.filter(title__icontains=filter_word).count()


    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_genre': num_genre,
        'filter_word': filter_word,
        'num_books_filtered': num_books_filtered,
    }

    # Render the HTML template index.html with the data in the context variable.
    return render(request, 'index.html', context=context)
