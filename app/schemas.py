
from typing import Optional
from pydantic import BaseModel, Field, constr

# Reglas de validación reutilizables
TitleStr = constr(min_length=1, max_length=200, strip_whitespace=True)
AuthorStr = constr(min_length=1, max_length=150, strip_whitespace=True)
# Validación simple de ISBN (10–17 chars, dígitos y guiones). Para la prueba es suficiente.
IsbnStr = constr(pattern=r"^[0-9\-]{10,17}$", strip_whitespace=True)


class BookBase(BaseModel):
    title: TitleStr = Field(..., description="Título del libro") # type: ignore
    author: AuthorStr = Field(..., description="Autor del libro")# type: ignore
    year: int = Field(..., ge=0, le=3000, description="Año de publicación (aprox. 0–3000)")
    isbn: IsbnStr = Field(..., description="ISBN (10–17, dígitos y guiones)") # type: ignore

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "Cien años de soledad",
                "author": "Gabriel García Márquez",
                "year": 1967,
                "isbn": "978-0307474728"
            }
        }
    }


class BookCreate(BookBase):
    """Payload para crear un libro."""
    pass


class BookUpdate(BaseModel):
    """Payload para actualizar un libro (parcial o total)."""
    title: Optional[TitleStr] = Field(None, description="Título del libro") # type: ignore
    author: Optional[AuthorStr] = Field(None, description="Autor del libro") # type: ignore
    year: Optional[int] = Field(None, ge=0, le=3000, description="Año de publicación")
    isbn: Optional[IsbnStr] = Field(None, description="ISBN") # type: ignore

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "Cien años de soledad (Edición Aniversario)",
                "year": 2017
            }
        }
    }


class BookRead(BaseModel):
    """Respuesta estándar al leer un libro."""
    id: int
    title: str
    author: str
    year: int
    isbn: str


    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": 1,
                "title": "Cien años de soledad",
                "author": "Gabriel García Márquez",
                "year": 1967,
                "isbn": "978-0307474728"
            }
        }
    }
