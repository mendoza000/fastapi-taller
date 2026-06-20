from fastapi import APIRouter, Depends, status

from ..database import get_db
from ..models import LibroCreate, LibroOut, LibroUpdate
from ..repositories import libros_repo

router = APIRouter(prefix="/libros", tags=["libros"])


@router.get("", response_model=list[LibroOut])
def listar(conn=Depends(get_db)):
    return libros_repo.listar(conn)


@router.get("/{libro_id}", response_model=LibroOut)
def obtener(libro_id: int, conn=Depends(get_db)):
    return libros_repo.obtener(conn, libro_id)


@router.post("", response_model=LibroOut, status_code=status.HTTP_201_CREATED)
def crear(data: LibroCreate, conn=Depends(get_db)):
    return libros_repo.crear(conn, data)


@router.put("/{libro_id}", response_model=LibroOut)
def actualizar(libro_id: int, data: LibroUpdate, conn=Depends(get_db)):
    return libros_repo.actualizar(conn, libro_id, data)


@router.delete("/{libro_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar(libro_id: int, conn=Depends(get_db)):
    libros_repo.eliminar(conn, libro_id)
