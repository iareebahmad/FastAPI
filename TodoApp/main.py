#main.py
from typing import Annotated
from fastapi import FastAPI, Depends
from fastapi.params import Depends
from models import Todos
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def read_all(db: Annotated[Session, Depends(get_db())]):
    return db.query(Todos).all()