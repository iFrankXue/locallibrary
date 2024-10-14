from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),

    # path('books/', views.books, name='books')
    
    # Using generic views
    path('books/', views.BookListView.as_view(), name='books'),
    path('books/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('authors/<int:pk>', views.AuthorDetailView.as_view(), name='author-detail')
]

urlpatterns += [
    path('mybooks/', views.LoanedBookByUserListView.as_view(), name='my-borrowed'),
    path('borrowed/', views.LoanedBookByAllUsersListView.as_view(), name='all-borrowed'),
]
