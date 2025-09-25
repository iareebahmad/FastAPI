from fastapi import Body, FastAPI

app = FastAPI()

BOOKS = [
    {'Title': 'Title One','Author': 'Author One', 'Category':'Science'},
    {'Title': 'Title Two','Author': 'Author Two','Category':'Science'},
    {'Title': 'Title Three','Author': 'Author Three','Category':'History'},
    {'Title': 'Title Four','Author': 'Author Four','Category':'Maths'},
    {'Title': 'Title Five', 'Author': 'Author Five','Category':'Maths'},
    {'Title': 'Title Six','Author': 'Author Two','Category':'Science'}
]

# GET METHODS
# Adding Endpoints

@app.get("/")
async def welcome_msg():
    return {"message": "Welcome to the Library"}

@app.get("/books")
async def read_all_books():
    #return {'message':'Ricardo Kaka rules'}
    return BOOKS

# Dynamic Param for books
# @app.get("/books/{dynamic_param}")
# async def read_all_books(dynamic_param: str):
#     return {'dynamic_param':dynamic_param}

# Order matter with path params: Since this comes after dynamic parameter, FastAPI will never run this.
# Instead, when you go to the API Endpoint, you'll find {'dynamic_param':'Your input'} as output and not {'book_title': 'Your input'}
# FastAPI looks at all fn from top to bottom and async def read_all_books(dynamic_param: str) comes first, so @app.get("/books/mybook") won't run
@app.get("/books/mybook")
async def read_all_books():
    return {'book_title': 'My Favourite Book!'}

# Shifting Dynamic Parameter to the last
# @app.get("/books/{dynamic_param}")
# async def read_all_books(dynamic_param: str):
#     return {'dynamic_param':dynamic_param}

# Path Parameter: A path parameter is a variable in the URL path that lets you pass dynamic values to your API endpoint.
@app.get("/books/{book_title}")
async def read_all_books(book_title :str):
    for book in BOOKS:
        if book.get('Title').casefold() == book_title.casefold():       # if Value from list == input value (check main.pt to understand .get() and .casefold()
            return book


# Query Parameter: Query Parameter is a key-value pair added to the end of a URL (after ?) to send extra information to an API endpoint.
#eg: LocalURL/books/?category=math
@app.get("/books/")
async def read_category_by_query(category :str):
    books_to_return = []
    for book in BOOKS:
        if book.get('Category').casefold() == category.casefold():
            books_to_return.append(book)
    return books_to_return

# Path Parameter + Query Parameter
# ex: LocalURL/books/author%20four/?category=science
#URL/Dynamic Path Param/ Query Param
@app.get("/books/{book_author}/")
async def read_category_by_query(book_author :str, category :str):
    books_to_return = []
    for book in BOOKS:
        if book.get('Author').casefold() == book_author.casefold() and book.get('Category').casefold() == category.casefold():
            books_to_return.append(book)
    return books_to_return

# typically : Path Param: TO find the location and Query Param: To Filter the data we want

# POST METHODS : Used to create data
@app.post("/books/create_book")
async def create_book(new_book=Body()):
    BOOKS.append(new_book)

# PUT Method: Used to Update Data, can have body like post.
# Changing category of author
@app.put("/books/update_book")
async def update_book(updated_book=Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('Title').casefold() == updated_book.get('Title').casefold():
            BOOKS[i] = updated_book

# DELETE Method: Used to delete data
@app.delete("/books/delete_book/{book_title}")
async def delete_book(book_title :str):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('Title').casefold() == book_title.casefold():
            BOOKS.pop(i)
            break

# Task : Create a new API Endpoint that can fetch all books from a specific author using either Path Parameters or Query Parameters.
#Path Parameter
# @app.get("/books/byauthor/{author}")
# async def book_by_author(author :str):
#     all_book_by_author = []
#     for book in BOOKS:
#         if book.get('Author').casefold() == author.casefold():
#             all_book_by_author.append(book)
#     return all_book_by_author

# Query Parameter
@app.get("/books/byauthor/")
async def book_by_author(author :str):
    all_book_by_author = []
    for book in BOOKS:
        if book.get('Author').casefold() == author.casefold():
            all_book_by_author.append(book)
    return all_book_by_author