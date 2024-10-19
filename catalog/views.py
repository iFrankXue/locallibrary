import datetime

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views import generic

from .forms import RenewBookForm, RenewBookModelForm
from .models import Book, Author, BookInstance, Genre, Country, Language

# Create your views here.

class BookListView(generic.ListView):
    model = Book
    context_object_name = 'book_list'
    paginate_by = 10

    # queryset = Book.objects.filter(title__icontains='var')[:5]
    def get_queryset(self):
        # return Book.objects.filter(title__icontains='war')[:5]
        return Book.objects.filter()
    

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

class LoanedBookByUserListView(LoginRequiredMixin, generic.ListView):
    """ Generic class-based view listing books on loan to current user. """
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return (
            BookInstance.objects
            .filter(borrower=self.request.user)
            .filter(status__exact='o')
            .order_by('due_back')
        )
    
class LoanedBookByAllUsersListView(PermissionRequiredMixin, generic.ListView):
    """ Permission required to specific users who has the permission. """
    permission_required = 'catalog.can_mark_returned'
    permission_denied_message = 'Sorry, you do not have permission to access this page.'
    raise_exception = False

    """ Generic class-based view listing books on loan to all users. """
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_all_users.html'
    paginate_by = 10

    def get_queryset(self):
        return (
            BookInstance.objects
            .filter(status__exact='o')
            .order_by('due_back')
        )
    
@login_required
@permission_required('catalog.can_renew', raise_exception=True)
def renew_book_librarian(request, pk):
    """ View function for renewing a specific BookInstance by librarian. """
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # If this is a POST request, then process the Form data.
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request(binding):
        # form = RenewBookForm(request.POST)   # replaced by ModelForm
        form = RenewBookModelForm(request.POST)

        # Check if the form is valid.
        if form.is_valid():
            # process the data in form.clean_data as required (here we just write it to the model due_back field)
            # book_instance.due_back = form.cleaned_data['renewal_date']  # replaced by ModelForm
            book_instance.due_back = form.cleaned_data['due_back']
            book_instance.save()

            # Redirect to a new URL:
            return HttpResponseRedirect(reverse('all-borrowed'))
    
    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookModelForm(initial={'due_back': proposed_renewal_date})
    
    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'catalog/book_renew_librarian.html', context)



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

""" Author Forms """

class AuthorCreate(PermissionRequiredMixin, CreateView):
    model = Author
    fields = ['first_name', 'last_name','country', 'date_of_birth', 'date_of_death']
    initial = {'date_of_death': '11/11/2023'}
    permission_required = 'catalog.add_author'

    # Example of using get_success_url to specify the success_url instead of using 
    # the get_absolute_url function defined in the Author Model.
    # It has the same function in this example, but if some different logic is 
    # needed, it is much useful.
    def get_success_url(self):
        return reverse('author-detail', kwargs={'pk': self.object.pk})


class AuthorUpdate(PermissionRequiredMixin, UpdateView):
    model = Author

    # Not recommended (potential security issue if more fields added)
    fields = '__all__'
    permission_required = 'catalog.change_author'


class AuthorDelete(PermissionRequiredMixin, DeleteView):
    model = Author
    success_url = reverse_lazy('authors')
    permission_required = 'catalog.delete_author'

    def form_valid(self, form):
        try:
            self.object.delete()
            return HttpResponseRedirect(self.success_url)
        except Exception as e:
            return HttpResponseRedirect(
                reverse('author-delete', kwargs={'pk': self.object.pk})
            )
        

""" Book Forms """

class BookCreate(PermissionRequiredMixin, CreateView):
    model = Book
    permission_required = 'catalog.add_book'
    fields = '__all__'
    
    def get_initial(self):
        english_language = Language.objects.get(name='English')
        return {'language': english_language}


class BookUpdate(PermissionRequiredMixin, UpdateView):
    model = Book
    permission_required = 'catalog.change_book'
    fields = '__all__'



class BookDelete(PermissionRequiredMixin, DeleteView):
    model = Book
    permission_required = 'catalog.delete_book'
    success_url = reverse_lazy('books')

    def form_valid(self, form):
        try:
            self.object.delete()
            return HttpResponseRedirect(self.success_url)
        except Exception as e:
            return HttpResponseRedirect(
                reverse('book-delete', kwargs={'pk':self.object.pk})
            ) 




