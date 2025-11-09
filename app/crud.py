
from typing import Iterable, Optional
from sqlalchemy import select
from sqlalchemy.orm import Session
from . import models
from .schemas import BookCreate, BookUpdate


def create_book(db: Session, data: BookCreate) -> models.Book:
    book = models.Book(
        title=data.title,
        author=data.author,
        year=data.year,
        isbn=data.isbn,
    )
    db.add(book)
    db.commit()
    db.refresh(book)
    return book


def list_books(
    db: Session,
    author: Optional[str] = None,
    year: Optional[int] = None,
    skip: int = 0,
    limit: int = 10
) -> Iterable[models.Book]:
    stmt = select(models.Book)
    if author:
        stmt = stmt.where(models.Book.author == author)
    if year is not None:
        stmt = stmt.where(models.Book.year == year)

    
    stmt = stmt.order_by(models.Book.id.asc()).offset(skip).limit(limit)

    
    return db.execute(stmt).scalars().all()


def get_book(db: Session, book_id: int) -> Optional[models.Book]:
    return db.get(models.Book, book_id)


def get_book_by_isbn(db: Session, isbn: str) -> Optional[models.Book]:
    stmt = select(models.Book).where(models.Book.isbn == isbn)
    return db.execute(stmt).scalar_one_or_none()


def update_book(db: Session, book_id: int, data: BookUpdate) -> Optional[models.Book]:
    book = db.get(models.Book, book_id)
    if not book:
        return None

    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(book, field, value)

    db.commit()
    db.refresh(book)
    return book


def delete_book(db: Session, book_id: int) -> bool:
    book = db.get(models.Book, book_id)
    if not book:
        return False
    db.delete(book)
    db.commit()
    return True


def search_books(db: Session, q: str) -> Iterable[models.Book]:

    from sqlalchemy import or_
    stmt = select(models.Book).where(
        or_(
            models.Book.title.ilike(f"%{q}%"),
            models.Book.author.ilike(f"%{q}%"),
        )
    )
    return db.execute(stmt).scalars().all()
