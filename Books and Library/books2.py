from fastapi import FastAPI, Body,Path,Query, HTTPException  #Path is used to validate path parameter ans Query for validating query params
from pydantic import BaseModel, Field       # Pydantic is used for validation of inputs
from typing import Optional
from starlette import status        #FastAPI is built using starlette, hence installing FastAPI means starlette is automatically installed

app = FastAPI()

class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: int

    #Constructor for the class
    def __init__(self,id,title,author,description,rating,published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date

# Book Request from Pydantic
class BookRequest(BaseModel):
    #Id : Optional[int] = None  # means it can either be null or zero. No need to pass any value in post req for id, id gets assigned because of py fn find_book_id()
    #or
    id : Optional[int] = Field(description='ID is not needed on create', default= None)
    title :str = Field(min_length=3)
    author :str = Field(min_length=1)
    description :str = Field(min_length=1, max_length=100)
    rating :int = Field(gt=1, lt=6)
    published_date: int = Field(gt=1995, lt=2040)
    # model_config adjusts the default values on swagger UI in Example Value section of the method
    """
    model_config in the BookRequest class helps define and enhance the input validation and representation of the request data in the Swagger documentation, making it easier for users to understand how to interact with your API effectively.
    """
    model_config = {
        "json_schema_extra":{
            "example":{
                "title":"A new book",
                "author":"codinwithroby",
                "description":"A new description",
                "rating": 5,
                "published_date": 2025

            }
        }
    }


BOOKS = [
    Book(1, 'Computer Science Pro', 'codingwithroby', 'A very nice book!', 5,1998),
    Book(2, 'Be Fast with FastAPI', 'codingwithroby', 'A great book!', 5,2012),
    Book(3, 'Master Endpoints', 'codingwithroby', 'A awesome book!', 5,2018),
    Book(4, 'HP1', 'Author 1', 'Book Description', 2,2019),
    Book(5, 'HP2', 'Author 2', 'Book Description', 3,2021),
    Book(6, 'HP3', 'Author 3', 'Book Description', 1,2024)
]

# API Endpoints
# Read all books
@app.get("/books", status_code=status.HTTP_200_OK)
async def read_all_books():
    return BOOKS

# Add a new book using Body()
# @app.post("/create-book")
# async def create_book(book_request = Body()):
#     BOOKS.append(book_request)

"""
Pydantic : It is a data library that is used for data modeling, data parsing and has efficient error handling.
It is commonly used as a resource for data validation and how to handle data coming to our FastAPI application.
Till now we were using Body() which has no data validation property, i.e. users can enter BookId as -900 and Rating as 99999 and still the system would accept it.
To put a check on this, we need Pydantic.
"""

# Add a new book using Pydantic for data validation
# #.model_dump() converts the request into a normal dictionary (like {"title": "Harry Potter", "author": "Rowling"}).
@app.post("/create-book", status_code=status.HTTP_201_CREATED)
async def create_book(book_request :BookRequest):
    new_book = Book(**book_request.model_dump()) # Book() creates an object of class Book and .model_dump converts the request to a normal dictionary
    BOOKS.append(find_book_id(new_book))


#  A normal py fn to increment id value by 1
def find_book_id(book: Book):
    book.id = 1 if len(BOOKS)==0 else BOOKS[-1].id +1 #Terany Optr
    # if len(BOOKS) > 0:
    #     book.id = BOOKS[-1].id +1
    # else:
    #     book.id = 1
    return book

# API Endpint
# Find a book based on Book id
@app.get("/books/{book_id}", status_code=status.HTTP_200_OK)
async def read_book(book_id: int = Path(gt=0)):         #Validating path params
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Item Not Found")

# Fetch books by rating
@app.get("/books/", status_code=status.HTTP_200_OK)                                         # Validating query param
async def read_book_by_rating(book_rating :int = Query(gt=0, lt=6)):
    books_to_return = []
    for book in BOOKS:
        if book.rating == book_rating:
            books_to_return.append(book)
    return books_to_return

# Update an exisiting book by Book id
@app.put("/books/update_book",status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book :BookRequest):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book
            book_changed = True
    if not book_changed:
        raise HTTPException(status_code=404,detail="Item Not Found")


# Delete a book
@app.delete("/books/{book_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id :int = Path(gt=0)):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            book_changed = True
            break
    if not book_changed:
        raise HTTPException(status_code=404,detail="Item Not Found")

# Fetch book by publication date
@app.get("/books/find_book/", status_code=status.HTTP_200_OK)
async def book_by_date(book_date: int = Query(gt=1995, lt=2040)):       # Validating query param
    booklist_by_date = []
    for book in BOOKS:
        if book.published_date == book_date:
            booklist_by_date.append(book)
    return booklist_by_date
"""
Status Code: Help Client to understand what happened on the server side application. They are international standards on how a client/server should HANDLE THE RESULT OF A REQUEST
- 1XX: Information Response: Request Processing
- 2XX: Success: Request Successfully Complete
    - 200: OK
    - 201: Created
    - 204: No Content (Used with PUT: Not returning anything but it changed something behind scenes on the server)
- 3XX: Redirection: Further Action must be complete
- 4XX: Client Errors: An error was caused by the client
    - 400: Bad Request : Used for invalid request methods
    - 401: Unauthorized
    - 404: Not Found
    - 422: Unprocessable Entity: Some sematic error in the request by the client
- 5XX: Server Errors: An error occurred in the server
    - 500 : Internal Server Error
"""