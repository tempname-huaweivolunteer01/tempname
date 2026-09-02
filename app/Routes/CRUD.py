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
# async def create_book(
#         book: Annotated[
#             CreateBookSchema,
#             Body(
#                 examples=[
#                     {
#                         "name": "foo",
#                         "author": "Foo Bar",
#                         "genre": "bar",
#                         "launch_date": "2008-09-15"
#                     }
#                     ]
#                 )
#             ]
#         ):

#     try: # Validação do formato de dados pedido, causa um erro se errado
#         _ = datetime.strptime(book.launch_date, "%Y-%m-%d")
#     except:
#         return HTTPException(status_code=400, detail="Invalid date format")

#     new_book = Book(
#             id=len(books),
#             name=book.name,
#             author=book.author,
#             genre=book.genre,
#             launch_date=book.launch_date
#             )

#     books.append(new_book)

#     return {
#             "message": "New book successfully created"
#             }

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
