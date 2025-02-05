# 📚 Library API (Django + DRF)

## 🌟 Overview
A RESTful API built with Django and Django REST Framework (DRF) for managing books, authors, and user favorite books. It includes:
- **User Authentication** (JWT-based login and token refresh)
- **Book & Author Management** (CRUD operations)
- **Search Functionality** (Search by book title or author)
- **Favorites List** (Add/remove books to favorites)
- **Recommendation System** (Suggest books based on user's favorites using a pre-trained `book_recommender.pkl` model)
- **Postman Collection** (Pre-configured for easy testing)

---

## 🚀 Features
- 🔐 **JWT Authentication**: Secure login and token management.
- 📖 **Book & Author API**: Create, read, update, and delete books & authors.
- 🔍 **Search**: Query books based on title or author.
- ❤️ **Favorites List**: Users can mark books as favorites (max 20).
- 🎯 **Recommendation System**: Suggests 5 similar books when a favorite is added.
- ⏳ **Optimized for Performance**: API responses return in **<1 second**.

---

## ⚙️ Installation Guide

### 1️⃣ Clone the Repository
```sh
git clone https://github.com/MFayizE/library-api-django.git
cd library-api-django
```

### 2️⃣ Set Up a Virtual Environment
```sh
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### 3️⃣ Install Dependencies
```sh
pip install -r requirements.txt
```

### 4️⃣ Apply Migrations & Create Superuser
```sh
python manage.py migrate
python manage.py createsuperuser
```

### 5️⃣ Run the Development Server
```sh
python manage.py runserver
```
API will be available at: `http://127.0.0.1:8000/api/`

---

## 🔑 Authentication (JWT)
- Register: `POST /api/register/`
- Login: `POST /api/login/`
- Refresh Token: `POST /api/token/refresh/`

### 📌 Example Login Request:
```json
{
    "username": "testuser",
    "password": "testpassword"
}
```

### 📌 Example Login Response:
```json
{
    "refresh": "your_refresh_token",
    "access": "your_access_token"
}
```

---

## 📌 API Endpoints

### 📚 **Books API**
| Method | Endpoint | Description |
|--------|-------------|--------------|
| GET | `/api/books/` | List all books |
| POST | `/api/books/` | Create a book |
| GET | `/api/books/{id}/` | Get book details |
| PUT | `/api/books/{id}/` | Update book |
| DELETE | `/api/books/{id}/` | Delete book |

### ✍ **Authors API**
| Method | Endpoint | Description |
|--------|-------------|--------------|
| GET | `/api/authors/` | List all authors |
| POST | `/api/authors/` | Create an author |
| GET | `/api/authors/{id}/` | Get author details |
| PUT | `/api/authors/{id}/` | Update author |
| DELETE | `/api/authors/{id}/` | Delete author |

### ❤️ **Favorites API**
| Method | Endpoint | Description |
|--------|-------------|--------------|
| POST | `/api/favorites/` | Add book to favorites |
| DELETE | `/api/favorites/` | Remove book from favorites |

### 🎯 **Book Recommendations**
- Each time a user adds a book to their favorites, **5 recommended books** are returned.
- Based on **content similarity** using a pre-trained **TF-IDF + Nearest Neighbors model (`book_recommender.pkl`)**.


### 🚀 Happy Coding! 🎉

