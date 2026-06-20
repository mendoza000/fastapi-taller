from datetime import date
from enum import Enum

from pydantic import BaseModel, Field, field_validator

from .validators import validar_anio, validar_email, validar_isbn


# --------------------------- Autores ---------------------------
class AutorBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=100)
    nacionalidad: str | None = Field(None, max_length=50)
    fecha_nacimiento: date | None = None


class AutorCreate(AutorBase):
    pass


class AutorUpdate(AutorBase):
    pass


class AutorOut(AutorBase):
    id: int


# --------------------------- Libros ----------------------------
class LibroBase(BaseModel):
    titulo: str = Field(..., min_length=1, max_length=200)
    isbn: str = Field(..., max_length=13)
    genero: str | None = Field(None, max_length=50)
    anio_publicacion: int | None = None
    autor_id: int

    @field_validator("isbn")
    @classmethod
    def _isbn(cls, v: str) -> str:
        return validar_isbn(v)

    @field_validator("anio_publicacion")
    @classmethod
    def _anio(cls, v: int | None) -> int | None:
        return validar_anio(v) if v is not None else v


class LibroCreate(LibroBase):
    pass


class LibroUpdate(LibroBase):
    pass


class LibroOut(LibroBase):
    id: int
    autor_nombre: str | None = None  # se completa con el JOIN a autores


# -------------------------- Usuarios ---------------------------
class UsuarioBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=100)
    email: str = Field(..., max_length=100)
    telefono: str | None = Field(None, max_length=20)

    @field_validator("email")
    @classmethod
    def _email(cls, v: str) -> str:
        return validar_email(v)


class UsuarioCreate(UsuarioBase):
    pass


class UsuarioOut(UsuarioBase):
    id: int


# -------------------------- Préstamos --------------------------
class EstadoPrestamo(str, Enum):
    activo = "activo"
    devuelto = "devuelto"
    vencido = "vencido"


class PrestamoCreate(BaseModel):
    libro_id: int
    usuario_id: int


class PrestamoOut(BaseModel):
    id: int
    libro_id: int
    usuario_id: int
    fecha_prestamo: date
    fecha_devolucion: date | None = None
    estado: EstadoPrestamo
