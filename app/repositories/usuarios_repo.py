import sqlite3

from ..exceptions import NotFoundError
from ..models import UsuarioCreate


def listar(conn: sqlite3.Connection) -> list[dict]:
    return [dict(r) for r in conn.execute("SELECT * FROM usuarios ORDER BY id").fetchall()]


def obtener(conn: sqlite3.Connection, usuario_id: int) -> dict:
    row = conn.execute("SELECT * FROM usuarios WHERE id = ?", (usuario_id,)).fetchone()
    if row is None:
        raise NotFoundError(f"No existe un usuario con id {usuario_id}")
    return dict(row)


def crear(conn: sqlite3.Connection, data: UsuarioCreate) -> dict:
    # Email duplicado -> IntegrityError UNIQUE -> 409 (handler global).
    cur = conn.execute(
        "INSERT INTO usuarios (nombre, email, telefono) VALUES (?, ?, ?)",
        (data.nombre, data.email, data.telefono),
    )
    conn.commit()
    return obtener(conn, cur.lastrowid)
