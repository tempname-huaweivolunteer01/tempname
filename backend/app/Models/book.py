from datetime import datetime, timezone

from sqlalchemy import DateTime, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column
from uuid import UUID, uuid4

from app.database.database import Base

class Book(Base):
    __tablename__ = "books"
    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(100))
    author: Mapped[str] = mapped_column(String(100))
    genre: Mapped[str] = mapped_column(String(100))
    launch_date: Mapped[str] = mapped_column(String(100))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    def __init__(self,
                 name:str,
                 author:str,
                 genre:str,
                 launch_date:str) -> None:
        self.name = name
        self.author = author
        self.genre = genre
        self.launch_date = launch_date

