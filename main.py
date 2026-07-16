from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

from fastapi import Depends, FastAPI, HTTPException, Response, status
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import create_tables, get_db
from models import Book as BookModel


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    create_tables()
    yield


app = FastAPI(title="Books API", lifespan=lifespan)


class BookCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    author: str = Field(min_length=1, max_length=120)
    published_year: int | None = Field(default=None, ge=0)
    isbn: str | None = Field(default=None, min_length=10, max_length=17)


class BookResponse(BookCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int


@app.get("/")
async def hello() -> dict[str, str]:
    """Return a simple greeting."""
    return {"message": "Hello"}


@app.get("/health")
async def health() -> dict[str, str]:
    """Report whether the API service is healthy."""
    return {"status": "ok"}


@app.post(
    "/books",
    response_model=BookResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["books"],
)
def create_book(book: BookCreate, db: Session = Depends(get_db)) -> BookModel:
    """Create a book in the configured database."""
    created_book = BookModel(**book.model_dump())
    db.add(created_book)
    db.commit()
    db.refresh(created_book)
    return created_book


@app.get("/books", response_model=list[BookResponse], tags=["books"])
def list_books(db: Session = Depends(get_db)) -> list[BookModel]:
    """Return all books."""
    statement = select(BookModel).order_by(BookModel.id)
    return list(db.scalars(statement).all())


def find_book(book_id: int, db: Session) -> BookModel:
    book = db.get(BookModel, book_id)
    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found",
        )
    return book


@app.get("/books/{book_id}", response_model=BookResponse, tags=["books"])
def get_book(book_id: int, db: Session = Depends(get_db)) -> BookModel:
    """Return a book by ID."""
    return find_book(book_id, db)


@app.put("/books/{book_id}", response_model=BookResponse, tags=["books"])
def update_book(
    book_id: int,
    book: BookCreate,
    db: Session = Depends(get_db),
) -> BookModel:
    """Replace an existing book."""
    existing_book = find_book(book_id, db)
    for field, value in book.model_dump().items():
        setattr(existing_book, field, value)
    db.commit()
    db.refresh(existing_book)
    return existing_book


@app.delete(
    "/books/{book_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["books"],
)
def delete_book(book_id: int, db: Session = Depends(get_db)) -> Response:
    """Delete a book by ID."""
    book = find_book(book_id, db)
    db.delete(book)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
