import sqlite3

import pytest
from fastapi.testclient import TestClient

from app.database import SCHEMA_PATH, get_db
from app.main import app


@pytest.fixture
def client(tmp_path):
    db_file = tmp_path / "test.db"

    # Crear el esquema en la base temporal.
    init_conn = sqlite3.connect(db_file)
    init_conn.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))
    init_conn.commit()
    init_conn.close()

    def override_get_db():
        conn = sqlite3.connect(db_file)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        try:
            yield conn
        finally:
            conn.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
