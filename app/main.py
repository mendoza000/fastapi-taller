from contextlib import asynccontextmanager

from fastapi import FastAPI

from .database import init_db
from .exceptions import register_exception_handlers
from .routers import autores, libros, prestamos, usuarios


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()  # crea las tablas al arrancar (idempotente)
    yield


app = FastAPI(
    title="Sistema de Gestión de Biblioteca",
    description="API RESTful CRUD sobre autores, libros, usuarios y préstamos. "
    "Taller práctico de Bases de Datos I.",
    version="1.0.0",
    lifespan=lifespan,
)

register_exception_handlers(app)

app.include_router(autores.router)
app.include_router(libros.router)
app.include_router(usuarios.router)
app.include_router(prestamos.router)


@app.get("/", tags=["root"])
def root():
    return {"mensaje": "API Biblioteca operativa. Documentación en /docs"}
