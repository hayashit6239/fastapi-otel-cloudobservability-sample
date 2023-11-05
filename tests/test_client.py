import pytest


@pytest.mark.asyncio
async def test_it(client):
    author1 = (await client.post("/authors?name=author1")).json()
    assert author1 == {"id": 1, "name": "author1"}, "POST /authors"

    authors = (await client.get("/authors")).json()
    assert authors == [author1], "GET /authors"

    actual = (await client.get("/authors/1")).json()
    assert actual == author1, "GET /authors/{author_id}"

    actual = (await client.put("/authors?author_id=1&name=test1")).json()
    assert actual == {"id": 1, "name": "test1"}, "PUT /authors"

    book1 = (await client.post("/books?name=book1&author_id=1")).json()
    assert book1 == {"id": 1, "name": "book1", "author_id": 1}, "POST /books"

    book2 = (await client.post("/books?name=book2&author_id=1")).json()
    assert book2 == {"id": 2, "name": "book2", "author_id": 1}, "POST /books"

    books = (await client.get("/books")).json()
    assert books == [book1, book2], "GET /books"

    actual = (await client.get("/books/2")).json()
    assert actual == book2, "GET /books/{book_id}"

    actual = (await client.get("/books/2/details")).json()
    expected = book2 | {"author": {"id": 1, "name": "test1"}}
    assert actual == expected, "GET /books/{book_id}/details"

    actual = (await client.put("/books?book_id=2&name=test2")).json()
    book2 |= {"name": "test2"}
    assert actual == book2, "PUT /books"

    await client.delete("/books?book_id=1")
    books = (await client.get("/books")).json()
    assert books == [book2], "DELETE /books"

    await client.delete("/authors?author_id=1")
    authors = (await client.get("/authors")).json()
    assert authors == [], "DELETE /authors"
    books = (await client.get("/books")).json()
    assert books == [], "CASCADE by DELETE /authors"
