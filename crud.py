from fastapi import FastAPI, status
from fastapi.exceptions import HTTPException
from pydantic import BaseModel

books = [
    {
      "id": 1,
      "title": "Atomic Habits",
      "author": "James Clear"
    },
    {
      "id": 2,
      "title": "The Alchemist",
      "author": "Paulo Coelho"
    },
    {
      "id": 3,
      "title": "Deep Work",
      "author": "Cal Newport"
    },
    {
      "id": 4,
      "title": "Sapiens",
      "author": "Yuval Noah Harari"
    },
    {
      "id": 5,
      "title": "Ikigai",
      "author": "Héctor García and Francesc Miralles"
    }
  ]

app = FastAPI()

@app.get("/books")
def get_all_books():
    return books

@app.get("/book/{book_id}")
def get_book(book_id:int):
    for book in books:
        if book['id'] == book_id:
            return book
    
    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Book not found")


class Book(BaseModel):
    id: int
    title: str
    author: str


@app.post("/book")
def create_book(book: Book):
    new_book = book.model_dump()
    books.append(new_book)


class BookUpdate(BaseModel):
    title: str
    author: str

@app.put("/book/{book_id}")
def create_book(book_id: int, book_update: BookUpdate):
    for book in books:
        if book['id'] == book_id:
            book['title'] == book_update.title
            book['author'] == book_update.author

@app.delete("/book/{book_id}")
def delete_book(book_id: int):
    for book in books:
        if book['id'] == book_id:
            books.remove(book)
            return {"Message": "Book is removed"}