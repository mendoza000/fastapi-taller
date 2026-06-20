from fastapi import APIRouter, Depends, status

from ..database import get_db
from ..models import UsuarioCreate, UsuarioOut
from ..repositories import usuarios_repo

router = APIRouter(prefix="/usuarios", tags=["usuarios"])


@router.get("", response_model=list[UsuarioOut])
def listar(conn=Depends(get_db)):
    return usuarios_repo.listar(conn)


@router.post("", response_model=UsuarioOut, status_code=status.HTTP_201_CREATED)
def crear(data: UsuarioCreate, conn=Depends(get_db)):
    return usuarios_repo.crear(conn, data)
