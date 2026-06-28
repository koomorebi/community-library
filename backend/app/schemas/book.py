from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel


class CategoryOut(BaseModel):
    id: int
    name: str
    sort_order: int

    model_config = {"from_attributes": True}


class CategoryCreate(BaseModel):
    name: str
    sort_order: int = 0


class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    sort_order: Optional[int] = None


class BookCopyOut(BaseModel):
    id: int
    copy_no: str
    book_location: Optional[str] = None
    status: str
    version: int

    model_config = {"from_attributes": True}


class BookCreate(BaseModel):
    title: str
    author: str
    isbn: str
    publisher: Optional[str] = None
    category_id: Optional[int] = None
    cover_image: Optional[str] = None
    description: Optional[str] = None
    total_copies: int = 1


class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    isbn: Optional[str] = None
    publisher: Optional[str] = None
    category_id: Optional[int] = None
    cover_image: Optional[str] = None
    description: Optional[str] = None


class BookOut(BaseModel):
    id: int
    title: str
    author: str
    isbn: str
    publisher: Optional[str] = None
    category_id: Optional[int] = None
    category: Optional[CategoryOut] = None
    cover_image: Optional[str] = None
    description: Optional[str] = None
    total_copies: int
    available_copies: int
    created_at: datetime
    updated_at: datetime
    copies: List[BookCopyOut] = []

    model_config = {"from_attributes": True}


class BookListOut(BaseModel):
    id: int
    title: str
    author: str
    isbn: str
    publisher: Optional[str] = None
    category: Optional[CategoryOut] = None
    cover_image: Optional[str] = None
    total_copies: int
    available_copies: int

    model_config = {"from_attributes": True}
