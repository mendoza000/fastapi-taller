import pytest


@pytest.fixture
def setup(client):
    autor_id = client.post("/autores", json={"nombre": "Autor"}).json()["id"]
    libro_id = client.post(
        "/libros",
        json={"titulo": "Libro", "isbn": "4444444444444", "anio_publicacion": 2010, "autor_id": autor_id},
    ).json()["id"]
    usuario_id = client.post(
        "/usuarios", json={"nombre": "Lector", "email": "lector@mail.com"}
    ).json()["id"]
    return {"libro_id": libro_id, "usuario_id": usuario_id}


def test_prestar_libro_ya_prestado_devuelve_409(client, setup):
    body = {"libro_id": setup["libro_id"], "usuario_id": setup["usuario_id"]}
    assert client.post("/prestamos", json=body).status_code == 201
    # Segundo préstamo del mismo libro estando activo -> 409.
    assert client.post("/prestamos", json=body).status_code == 409


def test_devolver_libera_y_permite_prestar_de_nuevo(client, setup):
    body = {"libro_id": setup["libro_id"], "usuario_id": setup["usuario_id"]}
    prestamo_id = client.post("/prestamos", json=body).json()["id"]

    resp = client.put(f"/prestamos/{prestamo_id}/devolver")
    assert resp.status_code == 200
    assert resp.json()["estado"] == "devuelto"

    # Ya devuelto -> se puede volver a prestar.
    assert client.post("/prestamos", json=body).status_code == 201


def test_prestamo_con_libro_inexistente_devuelve_400(client, setup):
    resp = client.post("/prestamos", json={"libro_id": 9999, "usuario_id": setup["usuario_id"]})
    assert resp.status_code == 400
