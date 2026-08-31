from datetime import datetime
from typing import Annotated
from fastapi import Body, HTTPException, APIRouter

from Schemas.schemas import CreateBookSchema, EditBookSchema

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
        raise HTTPException(status_code=400, detail="Invalid date format")

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
    
    raise HTTPException(status_code=400, detail="No book found for id provided")

@CRUD_ROUTER.get("/list")
async def list_books():
    return {"books": books}

@CRUD_ROUTER.put("/replace")
async def replace_book(
        book_id:int, 
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
    if book_id>len(books) or len(books) == 0:
        raise HTTPException(status_code=400, detail="BookID doesn't exist")

    try: # Validação do formato de dados pedido, causa um erro se errado
        _ = datetime.strptime(book.launch_date, "%Y-%m-%d")
    except:
        raise HTTPException(status_code=400, detail="Invalid date format")

    new_book = Book(
            id=book_id,
            name=book.name,
            author=book.author,
            genre=book.genre,
            launch_date=book.launch_date
            )

    books[book_id] = new_book

    return {
            "message": f"Book ({book_id}) replaced successfully"
            }

@CRUD_ROUTER.patch("/edit")
async def edit_book(book_id:int, schema:EditBookSchema):

    book:Book|None = None

    for book_entry in books:
        if book_entry.id == book_id:
            book = book_entry
    
    if not book:
        raise HTTPException(status_code=400, detail="No book found for id provided")

    if schema.launch_date:
        try: # Validação do formato de dados pedido, causa um erro se errado
            _ = datetime.strptime(book.launch_date, "%Y-%m-%d")
        except:
            raise HTTPException(status_code=400, detail="Invalid date format")

        book.launch_date = schema.launch_date

    if schema.genre:
        book.genre = schema.genre

    if schema.name:
        book.name = schema.name

    if schema.author:
        book.author = schema.author

    return {"message": "Book edited successfully"}

@CRUD_ROUTER.delete("/delete/{book_id}")
async def delete_book(book_id:int):
    indexer:int = 0

    for book in books:
        if book.id == book_id:
            return {
                    "message": "Book removed",
                    "book": books.pop(indexer)
                    }
        else:
            indexer += 1

    raise HTTPException(status_code=400, detail="No book found for id provided")
