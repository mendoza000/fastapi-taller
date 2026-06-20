import sqlite3

from ..database import iso
from ..exceptions import ConflictError, NotFoundError
from ..models import AutorCreate, AutorUpdate


def listar(conn: sqlite3.Connection, limit: int | None = None, offset: int = 0) -> list[dict]:
    sql = "SELECT * FROM autores ORDER BY id"
    params: list = []
    if limit is not None:  # paginación opcional
        sql += " LIMIT ? OFFSET ?"
        params = [limit, offset]
    return [dict(r) for r in conn.execute(sql, params).fetchall()]


def obtener(conn: sqlite3.Connection, autor_id: int) -> dict:
    row = conn.execute("SELECT * FROM autores WHERE id = ?", (autor_id,)).fetchone()
    if row is None:
        raise NotFoundError(f"No existe un autor con id {autor_id}")
    return dict(row)


def crear(conn: sqlite3.Connection, data: AutorCreate) -> dict:
    cur = conn.execute(
        "INSERT INTO autores (nombre, nacionalidad, fecha_nacimiento) VALUES (?, ?, ?)",
        (data.nombre, data.nacionalidad, iso(data.fecha_nacimiento)),
    )
    conn.commit()
    return obtener(conn, cur.lastrowid)


def actualizar(conn: sqlite3.Connection, autor_id: int, data: AutorUpdate) -> dict:
    obtener(conn, autor_id)  # lanza 404 si no existe
    conn.execute(
        "UPDATE autores SET nombre = ?, nacionalidad = ?, fecha_nacimiento = ? WHERE id = ?",
        (data.nombre, data.nacionalidad, iso(data.fecha_nacimiento), autor_id),
    )
    conn.commit()
    return obtener(conn, autor_id)


def eliminar(conn: sqlite3.Connection, autor_id: int) -> None:
    obtener(conn, autor_id)  # 404 si no existe
    # Regla de negocio: no borrar un autor con libros (ON DELETE RESTRICT).
    # Hacemos el chequeo explícito para devolver 409 con un mensaje claro,
    # en vez de dejar que la FK lance un IntegrityError genérico.
    n = conn.execute(
        "SELECT COUNT(*) AS c FROM libros WHERE autor_id = ?", (autor_id,)
    ).fetchone()["c"]
    if n > 0:
        raise ConflictError(
            f"No se puede eliminar el autor {autor_id}: tiene {n} libro(s) asociado(s)"
        )
    conn.execute("DELETE FROM autores WHERE id = ?", (autor_id,))
    conn.commit()
