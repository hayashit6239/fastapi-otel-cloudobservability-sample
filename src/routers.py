from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from . import functions
from .database import get_db
from .schemas import Author, Book, BookDetails

router = APIRouter()


@router.post("/authors", tags=["/authors"])
async def add_author(name: str, db: AsyncSession = Depends(get_db)) -> Author:
    author = await functions.add_author(name, db)
    return Author.model_validate(author)


@router.post("/books", tags=["/books"])
async def add_book(name: str, author_id: int, db: AsyncSession = Depends(get_db)) -> Book:
    book = await functions.add_book(name, author_id, db)
    if book is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Unknown author_id")
    return Book.model_validate(book)


@router.get("/authors", tags=["/authors"])
async def get_all_authors(db: AsyncSession = Depends(get_db)) -> list[Author]:
    authors = await functions.get_all_authors(db)
    return list(map(Author.model_validate, authors))


@router.get("/books", tags=["/books"])
async def get_all_books(db: AsyncSession = Depends(get_db)) -> list[Book]:
    books = await functions.get_all_books(db)
    return list(map(Book.model_validate, books))


@router.get("/authors/{author_id}", tags=["/authors"])
async def get_author(author_id: int, db: AsyncSession = Depends(get_db)) -> Author:
    author = await functions.get_author(author_id, db)
    if author is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Unknown author_id")
    return Author.model_validate(author)


@router.get("/books/{book_id}", tags=["/books"])
async def get_book(book_id: int, db: AsyncSession = Depends(get_db)) -> Book:
    book = await functions.get_book(book_id, db)
    if book is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Unknown book_id")
    return Book.model_validate(book)


@router.get("/books/{book_id}/details", tags=["/books"])
async def get_book_with_author(book_id: int, db: AsyncSession = Depends(get_db)) -> BookDetails:
    book = await functions.get_book_with_author(book_id, db)
    if book is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Unknown book_id")
    return BookDetails.model_validate(book)


@router.put("/authors", tags=["/authors"])
async def update_author(author_id: int, name: str, db: AsyncSession = Depends(get_db)) -> Author:
    author = await functions.update_author(author_id, name, db)
    if author is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Unknown author_id")
    return Author.model_validate(author)


@router.put("/books", tags=["/books"])
async def update_book(book_id: int, name: str, db: AsyncSession = Depends(get_db)) -> Book:
    book = await functions.update_book(book_id, name, db)
    if book is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Unknown book_id")
    return Book.model_validate(book)


@router.delete("/authors", tags=["/authors"])
async def delete_author(author_id: int, db: AsyncSession = Depends(get_db)):
    ok = await functions.delete_author(author_id, db)
    if not ok:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Unknown author_id")


@router.delete("/books", tags=["/books"])
async def delete_book(book_id: int, db: AsyncSession = Depends(get_db)):
    ok = await functions.delete_book(book_id, db)
    if not ok:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Unknown book_id")
