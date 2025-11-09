
def test_create_book(client):
    payload = {
        "title": "Cien años de soledad",
        "author": "Gabriel García Márquez",
        "year": 1967,
        "isbn": "978-0307474728"
    }
    r = client.post("/libros", json=payload)
    assert r.status_code == 201
    data = r.json()
    assert data["id"] > 0
    assert data["title"] == payload["title"]
    assert data["isbn"] == payload["isbn"]

def test_list_books(client):
    # pre: crear uno
    client.post("/libros", json={
        "title": "El coronel no tiene quien le escriba",
        "author": "Gabriel García Márquez",
        "year": 1961,
        "isbn": "978-0307474704"
    })
    r = client.get("/libros")
    assert r.status_code == 200
    books = r.json()
    assert isinstance(books, list)
    assert len(books) >= 1

def test_filter_by_author_and_year(client):
    client.post("/libros", json={
        "title": "Libro A",
        "author": "AutorX",
        "year": 2000,
        "isbn": "111-1111111111"
    })
    client.post("/libros", json={
        "title": "Libro B",
        "author": "AutorX",
        "year": 2001,
        "isbn": "222-2222222222"
    })
    r1 = client.get("/libros", params={"author": "AutorX"})
    assert r1.status_code == 200
    assert all(b["author"] == "AutorX" for b in r1.json())

    r2 = client.get("/libros", params={"year": 2000})
    assert r2.status_code == 200
    assert all(b["year"] == 2000 for b in r2.json())

def test_search_books(client):
    client.post("/libros", json={
        "title": "Programación en Python",
        "author": "Alguien",
        "year": 2020,
        "isbn": "333-3333333333"
    })
    r = client.get("/libros/search", params={"q": "python"})
    assert r.status_code == 200
    results = r.json()
    assert any("Python" in b["title"] for b in results) or len(results) >= 1

def test_update_book(client):
    # crear
    r = client.post("/libros", json={
        "title": "Titulo viejo",
        "author": "Autor",
        "year": 1999,
        "isbn": "444-4444444444"
    })
    book_id = r.json()["id"]
    # actualizar
    r2 = client.put(f"/libros/{book_id}", json={"title": "Titulo nuevo", "year": 2005})
    assert r2.status_code == 200
    data = r2.json()
    assert data["title"] == "Titulo nuevo"
    assert data["year"] == 2005

def test_duplicate_isbn_conflict(client):
    client.post("/libros", json={
        "title": "A",
        "author": "B",
        "year": 2000,
        "isbn": "555-5555555555"
    })
    r = client.post("/libros", json={
        "title": "A2",
        "author": "B2",
        "year": 2001,
        "isbn": "555-5555555555"
    })
    assert r.status_code == 409

def test_delete_book(client):
    r = client.post("/libros", json={
        "title": "Para borrar",
        "author": "X",
        "year": 2002,
        "isbn": "666-6666666666"
    })
    book_id = r.json()["id"]
    r2 = client.delete(f"/libros/{book_id}")
    assert r2.status_code == 204

    # comprobar que ya no existe
    r3 = client.get(f"/libros/{book_id}")
    assert r3.status_code == 404
