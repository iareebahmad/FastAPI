#models.py
"""
Now models is a way for SQL alchemy to be able to understand what kind of database tables we are going to be creating in the future
The Waiter = SQLAlchemy ORM
"""
from database import Base
from sqlalchemy import Integer, Column, String, Boolean


class Todos(Base):
    __tablename__ = 'todos'

    id = Column(Integer, primary_key= True, index = True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean, default=False)