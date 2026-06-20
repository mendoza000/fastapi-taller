def test_crear_y_obtener_autor(client):
    resp = client.post("/autores", json={"nombre": "Gabriel García Márquez", "nacionalidad": "Colombiana"})
    assert resp.status_code == 201
    autor = resp.json()
    assert autor["id"] > 0
    assert autor["nombre"] == "Gabriel García Márquez"

    resp = client.get(f"/autores/{autor['id']}")
    assert resp.status_code == 200
    assert resp.json()["nombre"] == "Gabriel García Márquez"


def test_obtener_autor_inexistente_devuelve_404(client):
    assert client.get("/autores/9999").status_code == 404


def test_crear_autor_sin_nombre_devuelve_422(client):
    # 'nombre' es obligatorio -> Pydantic rechaza antes de tocar la DB.
    assert client.post("/autores", json={"nacionalidad": "Argentina"}).status_code == 422


def test_no_se_puede_borrar_autor_con_libros(client):
    autor_id = client.post("/autores", json={"nombre": "Autor con libros"}).json()["id"]
    client.post(
        "/libros",
        json={"titulo": "Libro 1", "isbn": "1234567890123", "anio_publicacion": 2020, "autor_id": autor_id},
    )
    # ON DELETE RESTRICT + chequeo explícito -> 409 Conflict.
    assert client.delete(f"/autores/{autor_id}").status_code == 409
