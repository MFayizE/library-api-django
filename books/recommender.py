import pickle
import numpy as np
from django.core.cache import cache
from .models import Book

# Load model once at startup
model = None

def load_model():
    global model
    if model is None:
        cached_model = cache.get('book_recommender')
        if cached_model:
            model = cached_model
        else:
            with open('book_recommender.pkl', 'rb') as f:
                model = pickle.load(f)
            cache.set('book_recommender', model, timeout=86400)  # Cache for 1 day

def get_book_recommendations(favorite_books, num_recommendations=5):
    load_model()

    tfidf = model['tfidf']
    nn = model['nn']
    titles = np.array(model['titles'])  # Convert to NumPy array for faster lookup

    recommended_books = set()

    if not favorite_books:
        return []

    # Convert list of books to a TF-IDF vector
    book_vectors = tfidf.transform(favorite_books)

    # Compute the average vector and ensure it is a NumPy array
    avg_vector = np.asarray(np.mean(book_vectors, axis=0))  # ✅ Convert to NumPy array

    # Find similar books using Nearest Neighbors
    distances, indices = nn.kneighbors(avg_vector, n_neighbors=6)

    for i in indices[0]:
        if i < len(titles) and titles[i] not in favorite_books:
            recommended_books.add(titles[i])

    recommended_books = list(recommended_books)[:num_recommendations]

    # If not enough recommendations, add random books
    if len(recommended_books) < num_recommendations:
        random_books = list(Book.objects.exclude(title__in=recommended_books)
                                      .order_by('?')[:num_recommendations - len(recommended_books)])
        recommended_books.extend([book.title for book in random_books])

    return recommended_books
