"""
se mapea 404, 409, 400 que lanzamos a mano desde los repositorios.
"""

import sqlite3

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


class AppError(Exception):
    """Error de aplicación con un código HTTP asociado."""

    status_code = 500

    def __init__(self, detail: str):
        self.detail = detail
        super().__init__(detail)


class NotFoundError(AppError):
    status_code = 404


class ConflictError(AppError):
    status_code = 409


class BadRequestError(AppError):
    status_code = 400


def register_exception_handlers(app: FastAPI) -> None:
    """Registra los handlers globales en la app FastAPI."""

    @app.exception_handler(AppError)
    async def _app_error(request: Request, exc: AppError):
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

    @app.exception_handler(sqlite3.IntegrityError)
    async def _integrity(request: Request, exc: sqlite3.IntegrityError):
        # Inspeccionamos el mensaje de SQLite para decidir el código correcto.
        msg = str(exc).lower()
        if "unique" in msg:
            return JSONResponse(status_code=409, content={"detail": f"Violación de unicidad: {exc}"})
        if "foreign key" in msg:
            return JSONResponse(status_code=400, content={"detail": f"Referencia inválida (foreign key): {exc}"})
        if "check" in msg:
            return JSONResponse(status_code=422, content={"detail": f"Violación de restricción CHECK: {exc}"})
        if "not null" in msg:
            return JSONResponse(status_code=422, content={"detail": f"Campo obligatorio faltante: {exc}"})
        return JSONResponse(status_code=400, content={"detail": str(exc)})
