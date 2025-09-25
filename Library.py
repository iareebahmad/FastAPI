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
# GET Method for Welcome Page -- Simple Endpoints, No Parameters
@app.get("/")
async def welcome_msg():
    return {"message":"Welcome to The Grand Library"}

# GET Method for to see all books -- Simple Endpoints, No Parameters
@app.get("/books")
async def show_all_books():
    return BOOKS

# GET Method for to see all books -- Simple Endpoints, No Parameters
@app.get("/books/mybooks")
async def show_all_books():
    return {"book_title":"My Favourite Book"}

# Path Parameter
@app.get("/books/{dynamic_param}")
async def read_all_books(dynamic_param :str):
    return {"dynamic_param":dynamic_param}

# Query Parameter : Find Book Details based on Genre
@app.get("/books/")
async def read_by_genre(genre :str):
    books_to_return = []
    for book in BOOKS:
        if book.get('Genre').casefold() == genre.casefold():
            books_to_return.append(book)
    return books_to_return

# Path + Query Parameter
@app.get("/books/{author}/")
async def read_by_author_genre(author :str, genre :str):
    output_books = []
    for book in BOOKS:
        if book.get("Author").casefold() == author.casefold() and book.get('Genre').casefold() == genre.casefold():
            output_books.append(book)
    return output_books
