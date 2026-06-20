from fastapi import APIRouter, Depends, status

from ..database import get_db
from ..models import AutorCreate, AutorOut, AutorUpdate
from ..repositories import autores_repo

router = APIRouter(prefix="/autores", tags=["autores"])


@router.get("", response_model=list[AutorOut])
def listar(limit: int | None = None, offset: int = 0, conn=Depends(get_db)):
    return autores_repo.listar(conn, limit, offset)


@router.get("/{autor_id}", response_model=AutorOut)
def obtener(autor_id: int, conn=Depends(get_db)):
    return autores_repo.obtener(conn, autor_id)


@router.post("", response_model=AutorOut, status_code=status.HTTP_201_CREATED)
def crear(data: AutorCreate, conn=Depends(get_db)):
    return autores_repo.crear(conn, data)


@router.put("/{autor_id}", response_model=AutorOut)
def actualizar(autor_id: int, data: AutorUpdate, conn=Depends(get_db)):
    return autores_repo.actualizar(conn, autor_id, data)


@router.delete("/{autor_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar(autor_id: int, conn=Depends(get_db)):
    autores_repo.eliminar(conn, autor_id)
