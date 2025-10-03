#imports
from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from starlette import status

app = FastAPI()

#class
class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: int
    # Constructor initializing class attributes
    def __init__(self, id, title, author, description, rating, published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date

#Pydantic Class Basemodel
class BookRequest(BaseModel):
    id: Optional[int]  = Field(description='ID is not mandatory on creation', default=None)
    title: str = Field(min_length=3)
    author: str = Field(min_length=2)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=0, lt=6)
    published_date: int = Field(gt=1995, lt=2026)

    model_config = {
        "json_schema_extra":{
            "example":{
                "title":"Default Title",
                "author":"Default Author",
                "description": "This is the default dummy description",
                "rating": "5",
                "published_date": "2025",
            }
        }
    }

# Memory
BOOKS = [
    Book(1,"That Night","Nidhi Upadhyay","Psychological Thriller",4,2022),
    Book(2, "And The Mountains Echoed", "Khalid Hosseini","Tragedy",5,2019),
]


# API Endpoints/ Routes
#1. Read all books
@app.get("/books", status_code=status.HTTP_200_OK)
async def read_all_books():
    return BOOKS

#2. Add a new book using pydantic validation
@app.get("/books/create_book",status_code=status.HTTP_201_CREATED)
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    BOOKS.append(find_book_id(new_book))

# Adding id to the book
def find_book_id(book: Book):
    if len(BOOKS)>0:
        book.id = BOOKS[-1].id+1
    else:
        book.id = 1
    return book

#3. Find book based on Book ID
@app.get("/books/{book_id}")
async def find_by_book_id(book_id :int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book Not Found")

# Find books by rating -- Find and Filter
@app.get("/books/", status_code=status.HTTP_200_OK)
async def find_by_rating(book_rating: int = Query(gt=0, lt=6)):
    books_to_return = []
    for book in BOOKS:
        if book.rating == book_rating:
            books_to_return.append(book)
    return books_to_return

#4. Update an exsiting book by BookID
@app.put("/books/update_book", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book: BookRequest):
    book_flag = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book
            book_flag = True
    if not book_flag:
        raise HTTPException(status_code=404, detail='Item not found')

#5. Delete a book
@app.delete("/books/{book_id}",status_code=status.HTTP_200_OK)
async def delete_book(book_id: int = Path(gt=0)):
    flag = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            flag = True
            break
    if not flag:
        raise HTTPException(status_code=404, detail='Item not found')

#6. Fetch Book by publication date
@app.get("/books/find_book",status_code=status.HTTP_200_OK)
async def find_by_publication_date(book_date: int = Path(gt=1995, lt=2026)):
    book_list = []
    for book in BOOKS:
        if book.published_date == book_date:
            book_list.append(book)
    return book_list