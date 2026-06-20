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

## Endpoints

| Método | Endpoint | Descripción | Códigos |
|--------|----------|-------------|---------|
| GET | `/autores` | Listar autores (`?limit=&offset=` opcional) | 200 |
| GET | `/autores/{id}` | Obtener autor | 200, 404 |
| POST | `/autores` | Crear autor | 201, 422 |
| PUT | `/autores/{id}` | Actualizar autor | 200, 404, 422 |
| DELETE | `/autores/{id}` | Eliminar autor (si no tiene libros) | 204, 404, 409 |
| GET | `/libros` | Listar libros (incluye nombre del autor) | 200 |
| GET | `/libros/{id}` | Obtener libro | 200, 404 |
| POST | `/libros` | Crear libro | 201, 422, 400, 409 |
| PUT | `/libros/{id}` | Actualizar libro | 200, 404, 422, 400, 409 |
| DELETE | `/libros/{id}` | Eliminar libro (si no tiene préstamos) | 204, 404, 409 |
| GET | `/usuarios` | Listar usuarios | 200 |
| POST | `/usuarios` | Crear usuario | 201, 422, 409 |
| GET | `/prestamos` | Listar préstamos | 200 |
| POST | `/prestamos` | Registrar préstamo | 201, 400, 409 |
| PUT | `/prestamos/{id}/devolver` | Marcar como devuelto | 200, 404 |

## Decisiones de diseño y "trampas" del enunciado

Este enunciado tiene varias trampas. Así las resolvimos:

1. **`PRAGMA foreign_keys = ON` (la trampa #1).** SQLite **no** aplica foreign keys
   por defecto. Sin este PRAGMA en cada conexión, `ON DELETE RESTRICT` y todas las
   FKs no harían nada. Vive en `database.py::get_connection()`.

2. **Códigos HTTP `409` que la tabla del enunciado omite.** La tabla de endpoints
   no listaba `409` en `POST /libros`, `POST /usuarios` ni `DELETE /libros`, pero la
   Sección 7 sí lo exige (ISBN/email duplicado, borrar con dependencias).
   Implementamos según la lógica correcta de la Sección 7.

3. **"Libro ya prestado" no es una constraint de DB.** Es lógica de aplicación dentro
   de una transacción: se verifica que no haya un préstamo `activo` para ese libro
   ANTES de insertar, con `COMMIT`/`ROLLBACK` (`prestamos_repo.crear`).

4. **Año hardcodeado vs. dinámico.** El esquema fija `CHECK (anio <= 2026)`; la
   validación de la app usa el año actual (`datetime.now().year`). El CHECK queda
   como segunda barrera.

5. **FKs de `prestamos` sin `ON DELETE`.** El enunciado no las define; las declaramos
   `RESTRICT` explícitas para que el comportamiento sea consciente.

6. **Comillas en SQL.** El enunciado usa `DEFAULT "activo"` (comillas dobles), que en
   SQL estándar son identificadores, no cadenas. Usamos comillas simples (`'activo'`),
   que es lo correcto.

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
