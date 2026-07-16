from fastapi import FastAPI

from config import BOOKS, MOVIES

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
    myBooks = []
    for book in BOOKS:
        if str(book['author']).casefold() == author_name.casefold():
            myBooks.append(book)
    if len(myBooks) > 0:
        return {"Books": myBooks, "Total Books": len(myBooks)}
    else:
        return {"Books": [], "Total Books": 0}

@app.get("/books/view-by-lauguage/{language}")
async def get_books_by_language(language: str):
    """
    Searches for and retrieves books published in a specific language.
    
    The search is case-insensitive.

    Args:
        language (str): The language of the books to search for.

    Returns:
        dict: A dictionary containing the matched books and the total count.
    """
    myBooks = []
    for book in BOOKS:
        if str(book['language']).casefold() == language.casefold():
            myBooks.append(book)
    if len(myBooks) > 0:
        return {"Books": myBooks, "Total Books": len(myBooks)}
    else:
        return {"Books": [], "Total Books": 0}

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
    myBooks = []
    for book in BOOKS:
        if str(book['category']).casefold() == category.casefold():
            myBooks.append(book)
    if len(myBooks) > 0:
        return {"Books": myBooks, "Total Books": len(myBooks)}
    else:
        return {"Books": [], "Total Books": 0}


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

@app.get("/movies/get-by-lauguage/{language}")
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
    matched_movies = [movie for movie in MOVIES if str(movie['language']).casefold() == target_language]
    
    return {
        "Movies": matched_movies, 
        "Total Movies": len(matched_movies)
    }