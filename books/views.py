from rest_framework import generics, permissions
from .models import Book, Author, FavoriteBook
from .serializers import BookSerializer, AuthorSerializer, FavoriteBookSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from .recommender import get_book_recommendations
from django.db import transaction

class BookListCreateView(generics.ListCreateAPIView):
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Book.objects.all()
        search_query = self.request.query_params.get('search', None)
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) | Q(author__name__icontains=search_query)
            )
        return queryset

class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class AuthorListCreateView(generics.ListCreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class AuthorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

@api_view(['POST', 'DELETE'])
@permission_classes([permissions.IsAuthenticated])
def manage_favorites(request):
    user = request.user
    book_id = request.data.get('book_id')
    title = request.data.get('title')
    author_name = request.data.get('author')
    description = request.data.get('description')

    if not book_id and not (title and author_name and description):
        return Response({'error': 'Provide either book_id or full book details (title, author, description).'},
                        status=status.HTTP_400_BAD_REQUEST)

    with transaction.atomic():
        if book_id:
            try:
                book = Book.objects.get(id=book_id)
            except Book.DoesNotExist:
                return Response({'error': 'Book with the given ID not found.'}, status=status.HTTP_404_NOT_FOUND)
        else:
            author, _ = Author.objects.get_or_create(name=author_name)
            book, _ = Book.objects.get_or_create(title=title, author=author, defaults={'description': description})

    if request.method == 'POST':
        if FavoriteBook.objects.filter(user=user, book=book).exists():
            return Response({'message': 'Book already in favorites'}, status=status.HTTP_400_BAD_REQUEST)

        if FavoriteBook.objects.filter(user=user).count() >= 20:
            return Response({'error': 'Maximum of 20 favorite books allowed'}, status=status.HTTP_400_BAD_REQUEST)

        FavoriteBook.objects.create(user=user, book=book)

        favorite_books = FavoriteBook.objects.filter(user=user).select_related('book')
        favorite_titles = [fav.book.title for fav in favorite_books]

        recommendations = get_book_recommendations(favorite_titles)

        return Response({
            'message': 'Book added to favorites',
            'recommendations': recommendations
        }, status=status.HTTP_201_CREATED)

    elif request.method == 'DELETE':
        try:
            fav = FavoriteBook.objects.get(user=user, book=book)
            fav.delete()
            return Response({'message': 'Book removed from favorites'}, status=status.HTTP_200_OK)
        except FavoriteBook.DoesNotExist:
            return Response({'error': 'Book not in favorites'}, status=status.HTTP_400_BAD_REQUEST)