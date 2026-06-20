# Sistema de Gestión de Biblioteca — API CRUD

API RESTful con operaciones CRUD sobre **autores, libros, usuarios y préstamos**,
construida con **FastAPI + SQLite** (módulo `sqlite3`, sin ORM) y validaciones con
**Pydantic**. Taller práctico de Bases de Datos I.

## Requisitos

- Python 3.10 o superior

## Instalación

```bash
python -m venv .venv
# Windows (PowerShell):
.venv\Scripts\Activate.ps1
# Linux / macOS:
source .venv/bin/activate

pip install -r requirements.txt
```

## Ejecución

```bash
uvicorn app.main:app --reload --port 8000
```

- API: <http://localhost:8000>
- **Documentación interactiva (Swagger):** <http://localhost:8000/docs>
- La base `biblioteca.db` se crea sola al arrancar.

## Tests

```bash
pytest
```

Cada test corre contra una base SQLite temporal y aislada.

## Estructura

```
app/
  main.py            # crea la app, registra routers y handlers de error
  database.py        # conexión (PRAGMA foreign_keys=ON) e init del esquema
  schema.sql         # DDL de las 4 tablas con constraints
  exceptions.py      # errores de dominio + mapeo a códigos HTTP
  validators.py      # ISBN, email y año
  models.py          # modelos Pydantic (validación de entrada/salida)
  repositories/      # acceso a datos (SQL crudo + transacciones)
  routers/           # endpoints por entidad
tests/               # pruebas con TestClient
```

### Mapeo de errores

| Situación | Código |
|-----------|--------|
| Datos inválidos (tipo, longitud, formato ISBN/email/año) | 422 |
| Violación de `UNIQUE` (ISBN/email duplicado) | 409 |
| Violación de `FOREIGN KEY` (autor/libro/usuario inexistente) | 400 |
| Violación de `CHECK` | 422 |
| Recurso no encontrado | 404 |
| Regla de negocio (borrar con dependencias, libro ya prestado) | 409 |

## Exposición con Cloudflare Tunnel

```bash
cloudflared tunnel --url http://localhost:8000
```

Copiá la URL `https://*.trycloudflare.com` generada y compartila. Es temporal:
mantené el túnel activo durante la evaluación.

## Pruebas rápidas con curl

```bash
# Crear autor
curl -X POST http://localhost:8000/autores -H "Content-Type: application/json" \
  -d '{"nombre":"Jorge Luis Borges","nacionalidad":"Argentina"}'

# Crear libro
curl -X POST http://localhost:8000/libros -H "Content-Type: application/json" \
  -d '{"titulo":"Ficciones","isbn":"9780307474728","anio_publicacion":1944,"autor_id":1}'

# Registrar préstamo
curl -X POST http://localhost:8000/prestamos -H "Content-Type: application/json" \
  -d '{"libro_id":1,"usuario_id":1}'
```
