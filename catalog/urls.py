from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),

    # path('books/', views.books, name='books')
    
    # Using generic views
    path('books/', views.BookListView.as_view(), name='books'),
    path('books/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('author/<int:pk>', views.AuthorDetailView.as_view(), name='author-detail')
]

urlpatterns += [
    path('mybooks/', views.LoanedBookByUserListView.as_view(), name='my-borrowed'),
    path('borrowed/', views.LoanedBookByAllUsersListView.as_view(), name='all-borrowed'),
]

urlpatterns += [
    path('book/<uuid:pk>/renew/', views.renew_book_librarian, name='renew-book-librarian'),
]

urlpatterns += [
    path('author/create/', views.AuthorCreate.as_view(), name='author-create'),
    path('author/<int:pk>/update/', views.AuthorUpdate.as_view(), name='author-update'),
    path('author/<int:pk>/delete/', views.AuthorDelete.as_view(), name='author-delete'),
]

urlpatterns += [
    path('book/create/', views.BookCreate.as_view(), name='book-create'),
    path('book/<int:pk>/update', views.BookUpdate.as_view(), name='book-update'),
    path('book/<int:pk>/delete', views.BookDelete.as_view(), name='book-delete'),
]