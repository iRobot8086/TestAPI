import uuid
from datetime import date, datetime
from typing import Any, Dict, List, Optional, Required

from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import UUID4, BaseModel, Field, HttpUrl, ValidationError

from config import BOOKS, MOVIES


class Author(BaseModel):
    name: str
    country: str

class Dimensions(BaseModel):
    height: float
    width: float
    thickness: float
class BookRequest(BaseModel):
    
    
    title: str
    subtitle: Optional[str] = None
    original_title: Optional[str] = None
    
    author: Author
    co_authors: List[Author] = Field(default_factory=list)
    
    isbn13: str = Field(..., min_length=13, max_length=13)
    isbn10: str = Field(..., min_length=10, max_length=10)
    publisher: str
    publication_date: date
    edition: int = Field(default=1, ge=1)
    
    language: str
    available_languages: List[str]
    category: str
    sub_category: str
    genres: List[str]
    description: str
    
    selling_price_inr: float = Field(..., ge=0)
    mrp_inr: float = Field(..., ge=0)
    discount_percentage: float = Field(default=0, ge=0, le=100)
    currency: str
    
    global_rating: float = Field(default=0.0, ge=0.0, le=5.0)
    rating_count: int = Field(default=0, ge=0)
    review_count: int = Field(default=0, ge=0)
    copies_sold: int = Field(default=0, ge=0)
    pages: int = Field(..., gt=0)
    
    format: str
    dimensions_cm: Dimensions
    weight_grams: float = Field(..., gt=0)
    
    reading_level: str
    age_group: str
    awards: List[str] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)
    country_of_origin: str
    availability: str
    stock_quantity: int = Field(default=0, ge=0)
    
    ebook_available: bool
    audiobook_available: bool
    cover_image_url: Optional[str] = None
    preview_url: Optional[str] = None
    official_website: Optional[str] = None
    created_at: str = Field(default_factory=lambda: datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ"))
    



app = FastAPI(title="Data Sync API", version="0.1.0")

@app.get("/")
async def root():
    return {"message": "Welcome to the Sync Data API"}

@app.get("/health")
async def check_health():
    """
    Verifies the operational status of the API.

    Returns:
        dict: A status message indicating the API is running correctly.
    """
    return {"status": "healthy"}


@app.get("/books")
async def get_all_books():
    """
    Retrieves the complete catalog of books.

    Returns:
        dict: A dictionary containing the list of all available books.
    """
    return {"Books": BOOKS}


@app.get("/books/view-by-author/{author_name}")
async def get_books_by_author(author_name: str):
    """
    Searches for and retrieves books written by a specific author.
    
    The search is case-insensitive, allowing for flexible matching.

    Args:
        author_name (str): The name of the author to search for.

    Returns:
        dict: A dictionary containing the matched books and the total count.
    """
    target_author = author_name.casefold()
    myBooks = [
        book for book in BOOKS 
        if book.get('author', {}).get('name', '').casefold() == target_author
    ]
    
    return {"Books": myBooks, "Total Books": len(myBooks)}
    

@app.get("/books/view-by-title/{book_title}")
async def get_books_by_title(book_title: str):
    """
    Searches for a specific book based on its title.
    
    The search is case-insensitive, allowing for flexible matching.

    Args:
        book_title (str): Title of the book.

    Returns:
        dict: A dictionary containing the matched books and the total count.
    """
    target_title = book_title.casefold()
    myBooks = [
        book for book in BOOKS 
        if str(book['title']).casefold() == target_title
    ]
    
    return {"Books": myBooks, "Total Books": len(myBooks)}
    

@app.get("/books/view-by-language/{language}")
async def get_books_by_language(language: str):
    """
    Searches for and retrieves books published in a specific language.
    
    The search is case-insensitive.

    Args:
        language (str): The language of the books to search for.

    Returns:
        dict: A dictionary containing the matched books and the total count.
    """
    target_language = language.casefold()
    myBooks = [
        book for book in BOOKS 
        if book.get('language', '').casefold() == target_language
    ]
    
    return {"Books": myBooks, "Total Books": len(myBooks)}


@app.get("/books/get-by-language-and-genre/{language}")
async def get_books_by_language_and_genre(language: str, genre: str):
    """
    Searches for books by language (path) and genre (query).
    
    Example usage: /books/get-by-language-and-genre/spanish?genre=action
    """
    target_language = language.casefold()
    target_genre = genre.casefold()

    matched_books = [
        book for book in BOOKS 
        if book.get('language', '').casefold() == target_language 
        and any(g.casefold() == target_genre for g in book.get('genres', []))
    ]
    
    return {
        "Books": matched_books, 
        "Total Books": len(matched_books)
    }
    

@app.get("/books/view-by-category/{category}")
async def get_books_by_category(category: str):
    """
    Searches for and retrieves books belonging to a specific category.
    
    The search is case-insensitive.

    Args:
        category (str): The category or genre of the books to search for.

    Returns:
        dict: A dictionary containing the matched books and the total count.
    """
    target_category = category.casefold()
    myBooks = [
        book for book in BOOKS 
        if str(book['category']).casefold() == target_category
    ]
    
    return {"Books": myBooks, "Total Books": len(myBooks)}
    

@app.get("/movies")
async def get_all_movies():
    """
    Retrieves the complete catalog of movies.

    Returns:
        dict: A dictionary containing the list of all available movies.
    """
    return {"Movies": MOVIES}


@app.get("/movies/get-by-category/{category}")
async def get_movies_by_category(category: str):
    """
    Searches for movies that include a specific genre or category.
    
    The search safely checks against the list of genres associated with 
    each movie and is case-insensitive.

    Args:
        category (str): The genre or category to search for.

    Returns:
        dict: A dictionary containing the matched movies and the total count.
    """
    target_category = category.casefold()

    matched_movies = [
        movie for movie in MOVIES
        if any(genre.casefold() == target_category for genre in movie.get('genres', []))
    ]

    return {
        "Movies": matched_movies, 
        "Total Movies": len(matched_movies)
    }


@app.get("/movies/get-by-language/{language}")
async def get_movies_by_language(language: str):
    """
    Searches for and retrieves movies available in a specific language.
    
    The search is case-insensitive.

    Args:
        language (str): The language of the movies to search for.

    Returns:
        dict: A dictionary containing the matched movies and the total count.
    """
    target_language = language.casefold()
    matched_movies = [
        movie for movie in MOVIES 
        if movie.get('language', '').casefold() == target_language
    ]
    
    return {
        "Movies": matched_movies, 
        "Total Movies": len(matched_movies)
    }


@app.get("/movies/get-by-director/{director}")
async def get_movies_by_director(director: str):
    """
    Searches for and retrieves movies directed by a specific director.
    
    The search is case-insensitive.

    Args:
        director (str): The director of the movies to search for.

    Returns:
        dict: A dictionary containing the matched movies and the total count.
    """
    target_director = director.casefold()
    matched_movies = [
        movie for movie in MOVIES 
        if movie.get('director', '').casefold() == target_director
    ]
    
    return {
        "Movies": matched_movies, 
        "Total Movies": len(matched_movies)
    }

@app.post("/books/create-book")
async def Create_New_Book(new_book: BookRequest):
    book_dict = jsonable_encoder(new_book)
    book_dict['id'] = str(uuid.uuid4())
    BOOKS.append(book_dict)
    return {
        "status": status.HTTP_201_CREATED, 
        "message": "New book added successfully!",
        "book_id": book_dict["id"]
    }