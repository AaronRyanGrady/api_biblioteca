# app/routers/books.py
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from ..database import get_db
from .. import crud
from ..schemas import BookCreate, BookRead, BookUpdate

router = APIRouter(prefix="/libros", tags=["libros"])

@router.post(
    "",
    response_model=BookRead,
    status_code=status.HTTP_201_CREATED,
    summary="Agregar un libro",
)
def add_book(payload: BookCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_book(db, payload)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El ISBN ya existe.",
        )

@router.get(
    "",
    response_model=List[BookRead],
    summary="Listar libros  (con filtros y paginación)",
)
def list_books(
    author: Optional[str] = Query(None, description="Filtrar por autor exacto"),
    year: Optional[int] = Query(None, description="Filtrar por año exacto"),
    skip: int = Query(0, ge=0, description="Índice de inicio (offset)"),
    limit: int = Query(10, ge=1, le=100, description="Cantidad máxima de resultados"),
    db: Session = Depends(get_db),
):
    
    return crud.list_books(db, author=author, year=year, skip=skip, limit=limit)

# ⬇️ Mover /search ANTES de /{book_id}
@router.get(
    "/search",
    response_model=List[BookRead],
    summary="Buscar libros por título o autor (búsqueda parcial)",
)
def search(q: str = Query(..., min_length=1, description="Texto a buscar en título o autor"),
           db: Session = Depends(get_db)):
    return crud.search_books(db, q)

@router.get(
    "/{book_id}",
    response_model=BookRead,
    summary="Obtener un libro por ID",
)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = crud.get_book(db, book_id)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Libro no encontrado.")
    return book

@router.put(
    "/{book_id}",
    response_model=BookRead,
    summary="Actualizar información de un libro",
)
def update_book(book_id: int, payload: BookUpdate, db: Session = Depends(get_db)):
    try:
        book = crud.update_book(db, book_id, payload)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El ISBN ya existe.",
        )
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Libro no encontrado.")
    return book

@router.delete(
    "/{book_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar un libro",
)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    ok = crud.delete_book(db, book_id)
    if not ok:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Libro no encontrado.")
    return
