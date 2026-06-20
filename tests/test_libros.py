import pytest


@pytest.fixture
def autor_id(client):
    return client.post("/autores", json={"nombre": "Autor de prueba"}).json()["id"]


def test_crear_libro_ok_incluye_nombre_autor(client, autor_id):
    resp = client.post(
        "/libros",
        json={"titulo": "Cien años de soledad", "isbn": "9780307474728",
              "anio_publicacion": 1967, "autor_id": autor_id},
    )
    assert resp.status_code == 201
    assert resp.json()["autor_nombre"] == "Autor de prueba"  # viene del JOIN


def test_isbn_duplicado_devuelve_409(client, autor_id):
    libro = {"titulo": "A", "isbn": "1111111111111", "anio_publicacion": 2000, "autor_id": autor_id}
    assert client.post("/libros", json=libro).status_code == 201
    libro["titulo"] = "B"
    assert client.post("/libros", json=libro).status_code == 409  # UNIQUE


def test_isbn_invalido_devuelve_422(client, autor_id):
    resp = client.post(
        "/libros",
        json={"titulo": "X", "isbn": "123", "anio_publicacion": 2000, "autor_id": autor_id},
    )
    assert resp.status_code == 422  # no son 13 dígitos


def test_autor_inexistente_devuelve_400(client):
    # Requiere PRAGMA foreign_keys = ON para que la FK se aplique.
    resp = client.post(
        "/libros",
        json={"titulo": "X", "isbn": "2222222222222", "anio_publicacion": 2000, "autor_id": 9999},
    )
    assert resp.status_code == 400  # FOREIGN KEY


def test_anio_fuera_de_rango_devuelve_422(client, autor_id):
    resp = client.post(
        "/libros",
        json={"titulo": "X", "isbn": "3333333333333", "anio_publicacion": 3000, "autor_id": autor_id},
    )
    assert resp.status_code == 422  # año > actual
