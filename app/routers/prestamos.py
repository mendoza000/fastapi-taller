from fastapi import APIRouter, Depends, status

from ..database import get_db
from ..models import PrestamoCreate, PrestamoOut
from ..repositories import prestamos_repo

router = APIRouter(prefix="/prestamos", tags=["prestamos"])


@router.get("", response_model=list[PrestamoOut])
def listar(conn=Depends(get_db)):
    return prestamos_repo.listar(conn)


@router.post("", response_model=PrestamoOut, status_code=status.HTTP_201_CREATED)
def crear(data: PrestamoCreate, conn=Depends(get_db)):
    return prestamos_repo.crear(conn, data)


@router.put("/{prestamo_id}/devolver", response_model=PrestamoOut)
def devolver(prestamo_id: int, conn=Depends(get_db)):
    return prestamos_repo.devolver(conn, prestamo_id)
