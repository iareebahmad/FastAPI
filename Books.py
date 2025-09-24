from fastapi import FastAPI

app = FastAPI()

BOOKS = [
    {'Title': 'Title One','Author': 'Author One', 'Category':'Science'},
    {'Title': 'Title Two','Author': 'Author Two','Category':'Science'},
    {'Title': 'Title Three','Author': 'Author Three','Category':'History'},
    {'Title': 'Title Four','Author': 'Author Four','Category':'Maths'},
    {'Title': 'Title Five', 'Author': 'Author Five','Category':'Maths'},
    {'Title': 'Title Six','Author': 'Author Two','Category':'Maths'}
]
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

# Order matter with path params : Since this comes after dynamic parameter, FastAPI will never run this.
# Instead, when you go to the API Endpoint, you'll find {'dynamuc_param':'Your input'} as output and not {'book_title': 'Your input'}
# FastAPI looks at all fn from top to bottom and async def read_all_books(dynamic_param: str) comes first, so @app.get("/books/mybook") won't run
@app.get("/books/mybook")
async def read_all_books():
    return {'book_title': 'My Favourite Book!'}

# Shifting Dynamic Parameter to the last
@app.get("/books/{dynamic_param}")
async def read_all_books(dynamic_param: str):
    return {'dynamic_param':dynamic_param}