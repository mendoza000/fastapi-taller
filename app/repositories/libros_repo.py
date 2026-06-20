import sqlite3

from ..exceptions import ConflictError, NotFoundError
from ..models import LibroCreate, LibroUpdate

_SELECT = """
    SELECT l.id, l.titulo, l.isbn, l.genero, l.anio_publicacion,
           l.autor_id, a.nombre AS autor_nombre
    FROM libros l
    JOIN autores a ON a.id = l.autor_id
"""


def listar(conn: sqlite3.Connection) -> list[dict]:
    return [dict(r) for r in conn.execute(_SELECT + " ORDER BY l.id").fetchall()]


def obtener(conn: sqlite3.Connection, libro_id: int) -> dict:
    row = conn.execute(_SELECT + " WHERE l.id = ?", (libro_id,)).fetchone()
    if row is None:
        raise NotFoundError(f"No existe un libro con id {libro_id}")
    return dict(row)


def crear(conn: sqlite3.Connection, data: LibroCreate) -> dict:
    # ISBN duplicado -> IntegrityError UNIQUE -> 409 (handler global).
    # autor_id inexistente -> IntegrityError FOREIGN KEY -> 400 (handler global).
    cur = conn.execute(
        "INSERT INTO libros (titulo, isbn, genero, anio_publicacion, autor_id) "
        "VALUES (?, ?, ?, ?, ?)",
        (data.titulo, data.isbn, data.genero, data.anio_publicacion, data.autor_id),
    )
    conn.commit()
    return obtener(conn, cur.lastrowid)


def actualizar(conn: sqlite3.Connection, libro_id: int, data: LibroUpdate) -> dict:
    obtener(conn, libro_id)  # 404 si no existe
    conn.execute(
        "UPDATE libros SET titulo = ?, isbn = ?, genero = ?, "
        "anio_publicacion = ?, autor_id = ? WHERE id = ?",
        (data.titulo, data.isbn, data.genero, data.anio_publicacion, data.autor_id, libro_id),
    )
    conn.commit()
    return obtener(conn, libro_id)


def eliminar(conn: sqlite3.Connection, libro_id: int) -> None:
    obtener(conn, libro_id)  # 404 si no existe
    # La tabla de endpoints solo lista 204/404, pero borrar un libro con
    # préstamos rompe la integridad. Chequeo explícito -> 409.
    n = conn.execute(
        "SELECT COUNT(*) AS c FROM prestamos WHERE libro_id = ?", (libro_id,)
    ).fetchone()["c"]
    if n > 0:
        raise ConflictError(
            f"No se puede eliminar el libro {libro_id}: tiene {n} préstamo(s) asociado(s)"
        )
    conn.execute("DELETE FROM libros WHERE id = ?", (libro_id,))
    conn.commit()
