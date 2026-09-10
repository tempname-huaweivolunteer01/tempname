from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, String, UniqueConstraint, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import UUID, uuid4

from app.database.database import Base

# class Book(Base):
#     __tablename__ = "books"
#     id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
#     name: Mapped[str] = mapped_column(String(100))
#     author: Mapped[str] = mapped_column(String(100))
#     genre: Mapped[str] = mapped_column(String(100))
#     launch_date: Mapped[str] = mapped_column(String(100))
#     created_at: Mapped[datetime] = mapped_column(
#         DateTime(timezone=True),
#         default=lambda: datetime.now(timezone.utc),
#         nullable=False
#     )

#     def __init__(self,
#                  name:str,
#                  author:str,
#                  genre:str,
#                  launch_date:str) -> None:
#         self.name = name
#         self.author = author
#         self.genre = genre
#         self.launch_date = launch_date
class User(Base):
    __tablename__ = "users"
    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(100), nullable=False)
    workspace_memberships: Mapped[list["WorkspaceMember"]] = relationship(back_populates="user")

class Workspace(Base):
    __tablename__ = "workspaces"
    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    owner_id: Mapped[UUID] = mapped_column(Uuid, ForeignKey("users.id"), nullable=False)
    owner: Mapped["User"] = relationship()
    members: Mapped[list["WorkspaceMember"]] = relationship(back_populates="workspace")
    projects: Mapped[list["Project"]] = relationship(back_populates="workspace")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )
    logo_url: Mapped[str] = mapped_column(String(100))

class WorkspaceMember(Base):
    __tablename__ = "workspace_members"
    __table_args__ = (
        UniqueConstraint(
            "workspace_id",
            "user_id",
            name="uq_workspace_member"
        ),
    )
    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    workspace_id: Mapped[UUID] = mapped_column(Uuid, ForeignKey("workspaces.id"), nullable=False)
    user_id: Mapped[UUID] = mapped_column(Uuid, ForeignKey("users.id"), nullable=False)
    role: Mapped[str] = mapped_column(String(100), nullable=False)
    workspace: Mapped["Workspace"] = relationship(back_populates="members")
    user: Mapped["User"] = relationship(back_populates="workspace_memberships")

class Project(Base):
    __tablename__ = "projects"
    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    workspace_id: Mapped[UUID] = mapped_column(Uuid, ForeignKey("workspaces.id"), nullable=False)
    workspace: Mapped["Workspace"] = relationship(back_populates="projects")
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(100), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )
    color: Mapped[str] = mapped_column(String(100), nullable=False)
    icon_url: Mapped[str] = mapped_column(String(100), nullable=True)

