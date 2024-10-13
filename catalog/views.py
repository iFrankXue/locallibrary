from django.shortcuts import render
from django.http import HttpResponse
from .models import Book, Author, BookInstance, Genre, Country

from django.views import generic

# Create your views here.

class BookListView(generic.ListView):
    model = Book
    context_object_name = 'book_list'
    paginate_by = 3

    # queryset = Book.objects.filter(title__icontains='var')[:5]
    def get_queryset(self):
        # return Book.objects.filter(title__icontains='war')[:5]
        return Book.objects.filter()[:5]
    

    # Demo for changing the get_context_data function
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        # context = super(BookListView, self).get_context_data(**kwargs)
        # No need to specify the class name and self in Python3
        context = super().get_context_data(**kwargs)

        # Create any data and add it to the context
        context['some_data'] = 'This is some data'
        return context

    
class BookDetailView(generic.DetailView):
    model = Book


class AuthorListView(generic.ListView):
    model = Author


class AuthorDetailView(generic.DetailView):
    model = Author
    
    # def get_context_data(self):
    #     return Book.objects.all().annotate(available_count = models.Count('bookinstance', filter=models.Q(bookinstance__status='a')))


def index(request):
    # return HttpResponse("This is the context from catalog index.")
    # Generate counts of some of the main objects.
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # The 'all()' is implied by default.
    num_authors = Author.objects.count()

    # Number of visitors to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    num_visits += 1
    request.session['num_visits'] = num_visits

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
        'num_visits': num_visits,
    }

    # Render the HTML template index.html with the data in the context variable.
    return render(request, 'index.html', context=context)


