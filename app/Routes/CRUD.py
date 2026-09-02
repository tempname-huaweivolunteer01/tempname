from datetime import datetime
from typing import Annotated, List
from fastapi import Body, Depends, HTTPException, APIRouter
from uuid import UUID, uuid4
from sqlalchemy.orm import Session

from app.Schemas.schemas import BookResponseSchema, CreateBookSchema
from app.database.database import get_session

from app.Models.book import Book
from app.Repositories.static_storage import BookRepository

CRUD_ROUTER = APIRouter()
SessionDep = Annotated[Session, Depends(get_session)]

@CRUD_ROUTER.post("/", response_model=BookResponseSchema)
async def create_book(book: CreateBookSchema, session: SessionDep) -> BookResponseSchema:
    repo = BookRepository(session)
    try: # Validação do formato de dados pedido, causa um erro se errado
        _ = datetime.strptime(book.launch_date, "%Y-%m-%d")
    except:
        raise HTTPException(status_code=400, detail="Invalid date format")

    return repo.create_book(book.name, book.author, book.genre, book.launch_date)

@CRUD_ROUTER.get("/{book_id}", response_model=BookResponseSchema)
async def read_single_book(book_id: UUID, session: SessionDep) -> BookResponseSchema:
    repo = BookRepository(session)
    book = repo.get_by_id(book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="no book found for id provided")
    return book

@CRUD_ROUTER.get("/", response_model=List[BookResponseSchema])
async def list_books(session: SessionDep) -> List[BookResponseSchema]:
    repo = BookRepository(session)
    return repo.get_all()

# TODO: integrar com a base de dados
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

# TODO: integrar com base de dados
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

# TODO: integrar com base de dados
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
