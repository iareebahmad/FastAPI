from fastapi import Body, FastAPI

app = FastAPI()

BOOKS = [
    {'Name':'Harry Potter','Author':'J.K Rowling','Genre':'Fiction'},
    {'Name':'Game of Thrones','Author':'George R. R. Martin','Genre':'Fiction'},
    {'Name':'A Thousand Splendid Suns','Author':'Khalid Hosseini','Genre':'Fiction'},
    {'Name':'Let Us Python','Author':'Yashvant Kanetkar','Genre':'Educational'},
    {'Name':'Wings Of Fire','Author':'A.P.J Abdul Kalam','Genre':'Autobiography'},
    {'Name':'Geography','Author':'NCERT','Genre':'Educational'},
    {'Name':'Dreams From My Father','Author':'Barack Obama','Genre':'Autobiography'},
    {'Name':'The Kite Runner','Author':'Khalid Hosseini','Genre':'Fiction'}
]

# -------------------------------
# GET Methods
# -------------------------------

@app.get("/")
async def welcome_msg():
    return {"message":"Welcome to The Grand Library"}

@app.get("/books")
async def show_all_books():
    return BOOKS

@app.get("/books/mybooks")
async def show_favorite_book():
    return {"book_title":"My Favourite Book"}

# Get books by genre (Query Parameter)
@app.get("/books/by_genre")
async def get_books_by_genre(genre: str):
    return [book for book in BOOKS if book['Genre'].casefold() == genre.casefold()]

# Get books by author (Path Parameter)
@app.get("/books/by_author/{authorname}")
async def get_books_by_author(authorname: str):
    return [book for book in BOOKS if book['Author'].casefold() == authorname.casefold()]

# -------------------------------
# POST Method: Add new book
# -------------------------------
@app.post("/books")
async def add_new_book(new_book = Body()):
    BOOKS.append(new_book)
    return new_book

# -------------------------------
# PUT Method: Update book details
# -------------------------------
@app.put("/books/{book_name}")
async def update_book(book_name: str, updated_book = Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i]['Name'].casefold() == book_name.casefold():
            BOOKS[i] = updated_book
            return updated_book

# -------------------------------
# DELETE Method: Delete a book
# -------------------------------
@app.delete("/books/{book_name}")
async def delete_book(book_name: str):
    for i in range(len(BOOKS)):
        if BOOKS[i]['Name'].casefold() == book_name.casefold():
            return BOOKS.pop(i)

# Get books by a specific author (dynamic Path Parameter)
@app.get("/books/author/{author_name}")
async def get_books_by_author_dynamic(author_name: str):
    author_books = []
    for book in BOOKS:
        if book['Author'].casefold() == author_name.casefold():
            author_books.append(book)
    return author_books
