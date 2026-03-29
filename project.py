"""
FASTAPI APPLICATION FILE

Purpose:
---------
This file defines the API endpoints for interacting with the database.

What this file does:
--------------------
1. Creates FastAPI app
2. Defines request schema using Pydantic
3. Implements API routes (POST, GET)
4. Uses SQLAlchemy session to interact with database

Key Concepts:
-------------
- FastAPI → Web framework to build APIs
- Pydantic Model → Validates request/response data
- SQLAlchemy Model → Represents DB table
- Dependency Injection → get_db provides DB session automatically

Important Distinction:
----------------------
- Pydantic Model (Bookstore) → Used for API validation
- SQLAlchemy Model (Book) → Used for database operations

Flow of POST /books:
--------------------
Client Request → FastAPI → Validate using Pydantic →
Create SQLAlchemy object → Add to DB → Commit → Return response

Flow of GET /books:
-------------------
Client Request → FastAPI → Query DB → Return all books

Example API:
------------
POST /books → Add a book
GET /books → Fetch all books

Run server:
-----------
uvicorn main:app --reload

Access API docs:
----------------
http://127.0.0.1:8000/docs
"""


from fastapi import FastAPI, Depends
from database import get_db, engine
from sqlalchemy.orm import Session 
from pydantic import BaseModel
import model

app = FastAPI()

class Bookstore(BaseModel):
    id: int
    title: str
    author: str


@app.post("/books")
def create_book(book:Bookstore, db: Session = Depends(get_db)):
    new_book = model.Book(id = book.id, title = book.title, author = book.author)
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book


@app.get("/books")
def get_books(db: Session = Depends(get_db)):
    books = db.query(model.Book).all()
    return books