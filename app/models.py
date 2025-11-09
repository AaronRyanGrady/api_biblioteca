
from sqlalchemy import String, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from .database import Base

class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(200), index=True)
    author: Mapped[str] = mapped_column(String(150), index=True)
    year: Mapped[int] = mapped_column(Integer)
    isbn: Mapped[str] = mapped_column(String(20), unique=True, index=True)

    __table_args__ = (
        UniqueConstraint("isbn", name="uq_books_isbn"),
    )
