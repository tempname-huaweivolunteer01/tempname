from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID

from app.Models.book import Book

class BookRepository:
    def __init__(self, session: Session):
        self.session = session

    def create_book(self, name: str, author: str, genre: str, launch_date: str):
        new_book = Book(name, author, genre, launch_date)
        self.session.add(new_book)
        self.session.commit()
        self.session.refresh(new_book)
        return new_book

    def get_by_id(self, book_id: UUID) -> Optional[Book]:
        return self.session.query(Book).filter(Book.id == book_id).first()

    def get_all(self) -> List[Book]:
        return self.session.query(Book).all()
