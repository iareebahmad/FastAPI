from fastapi import FastAPI, Body
from pydantic import BaseModel, Field
from typing import Optional
app = FastAPI()

class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int

    #Constructor for the class
    def __init__(self,id,title,author,description,rating):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating

# Book Request from Pydantic
class BookRequest(BaseModel):
    id : Optional[int] = None  # means it can either be null or zero. No need to pass any value in post req for id, id gets assigned because of py fn find_book_id()
    title :str = Field(min_length=3)
    author :str = Field(min_length=1)
    description :str = Field(min_length=1, max_length=100)
    rating :int = Field(gt=-1, lt=6)


BOOKS = [
    Book(1, 'Computer Science Pro', 'codingwithroby', 'A very nice book!', 5),
    Book(2, 'Be Fast with FastAPI', 'codingwithroby', 'A great book!', 5),
    Book(3, 'Master Endpoints', 'codingwithroby', 'A awesome book!', 5),
    Book(4, 'HP1', 'Author 1', 'Book Description', 2),
    Book(5, 'HP2', 'Author 2', 'Book Description', 3),
    Book(6, 'HP3', 'Author 3', 'Book Description', 1)
]

# API Endpoints
# Read all books
@app.get("/books")
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
@app.post("/create-book")
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