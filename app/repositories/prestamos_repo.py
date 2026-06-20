import sqlite3

from ..exceptions import BadRequestError, ConflictError, NotFoundError
from ..models import PrestamoCreate


def listar(conn: sqlite3.Connection) -> list[dict]:
    return [dict(r) for r in conn.execute("SELECT * FROM prestamos ORDER BY id").fetchall()]


def obtener(conn: sqlite3.Connection, prestamo_id: int) -> dict:
    row = conn.execute("SELECT * FROM prestamos WHERE id = ?", (prestamo_id,)).fetchone()
    if row is None:
        raise NotFoundError(f"No existe un préstamo con id {prestamo_id}")
    return dict(row)


def crear(conn: sqlite3.Connection, data: PrestamoCreate) -> dict:
    try:
        # 1) El libro debe existir
        if conn.execute("SELECT 1 FROM libros WHERE id = ?", (data.libro_id,)).fetchone() is None:
            raise BadRequestError(f"No existe un libro con id {data.libro_id}")

        # 2) El usuario debe existir
        if conn.execute("SELECT 1 FROM usuarios WHERE id = ?", (data.usuario_id,)).fetchone() is None:
            raise BadRequestError(f"No existe un usuario con id {data.usuario_id}")

        # 3) El libro no puede tener un préstamo activo
        activos = conn.execute(
            "SELECT COUNT(*) AS c FROM prestamos WHERE libro_id = ? AND estado = 'activo'",
            (data.libro_id,),
        ).fetchone()["c"]
        if activos > 0:
            raise ConflictError(f"El libro {data.libro_id} ya está prestado (préstamo activo)")

        # 4) Todo OK -> insertar y confirmar la transacción.
        cur = conn.execute(
            "INSERT INTO prestamos (libro_id, usuario_id) VALUES (?, ?)",
            (data.libro_id, data.usuario_id),
        )
        conn.commit()
        return obtener(conn, cur.lastrowid)
    except Exception:
        # Cualquier fallo deshace cambios pendientes y se relanza para que el
        # handler global traduzca la excepción al código HTTP correcto.
        conn.rollback()
        raise


def devolver(conn: sqlite3.Connection, prestamo_id: int) -> dict:
    obtener(conn, prestamo_id)  # 404 si no existe
    conn.execute(
        "UPDATE prestamos SET estado = 'devuelto', fecha_devolucion = CURRENT_DATE WHERE id = ?",
        (prestamo_id,),
    )
    conn.commit()
    return obtener(conn, prestamo_id)
