from datetime import datetime
from typing import Annotated
from fastapi import Body, HTTPException, APIRouter

from Schemas.schemas import CreateBookSchema

from Models.book import Book
from Repositories.static_storage import books

CRUD_ROUTER = APIRouter()

@CRUD_ROUTER.post("/create")
async def create_book(
        book: Annotated[
            CreateBookSchema,
            Body(
                examples=[
                    {
                        "name": "foo",
                        "author": "Foo Bar",
                        "genre": "bar",
                        "launch_date": "2008-09-15"
                    }
                    ]
                )
            ]
        ):

    try: # Validação do formato de dados pedido, causa um erro se errado
        _ = datetime.strptime(book.launch_date, "%Y-%m-%d")
    except:
        return HTTPException(status_code=400, detail="Invalid date format")

    new_book = Book(
            id=len(books),
            name=book.name,
            author=book.author,
            genre=book.genre,
            launch_date=book.launch_date
            )

    books.append(new_book)

    return {
            "message": "New book successfully created"
            }

@CRUD_ROUTER.get("/list/{book_id}")
async def read_single_book(book_id:int):
    # temp
    for book in books:
        if book.id == book_id:
            return {"book": book}
    
    raise HTTPException(status_code=400, detail="no book found for id provided")

@CRUD_ROUTER.get("/list")
async def list_books():
    return {"books": books}
