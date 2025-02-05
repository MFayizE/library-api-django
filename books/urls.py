from django.urls import path
from .views import BookListCreateView, BookDetailView, AuthorListCreateView, AuthorDetailView,manage_favorites

urlpatterns = [
    path('books/', BookListCreateView.as_view()),
    path('books/<int:pk>/', BookDetailView.as_view()),
    path('authors/', AuthorListCreateView.as_view()),
    path('authors/<int:pk>/', AuthorDetailView.as_view()),
    path('favorites/', manage_favorites, name='manage_favorites'),
]
