from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.book import Book
from app.models.book_copy import BookCopy
from app.models.category import Category
from app.schemas.book import (
    BookCreate, BookUpdate, BookOut, BookListOut,
    CategoryCreate, CategoryUpdate, CategoryOut,
)
from app.schemas.common import success_response, error_response

router = APIRouter(prefix="/api/v1", tags=["图书管理"])


# ── 分类 ──────────────────────────────────────────────

@router.get("/categories", summary="获取分类列表")
def list_categories(db: Session = Depends(get_db)):
    cats = db.query(Category).order_by(Category.sort_order, Category.id).all()
    return success_response(data=[CategoryOut.model_validate(c).model_dump() for c in cats])


@router.post("/categories", summary="新增分类")
def create_category(req: CategoryCreate, db: Session = Depends(get_db)):
    existing = db.query(Category).filter(Category.name == req.name).first()
    if existing:
        return error_response(400, "分类名称已存在")
    cat = Category(name=req.name, sort_order=req.sort_order)
    db.add(cat)
    db.commit()
    db.refresh(cat)
    return success_response(data=CategoryOut.model_validate(cat).model_dump())


@router.put("/categories/{category_id}", summary="修改分类")
def update_category(category_id: int, req: CategoryUpdate, db: Session = Depends(get_db)):
    cat = db.query(Category).filter(Category.id == category_id).first()
    if not cat:
        return error_response(404, "分类不存在")
    if req.name and req.name != cat.name:
        dup = db.query(Category).filter(Category.name == req.name, Category.id != category_id).first()
        if dup:
            return error_response(400, "分类名称已存在")
    for field, value in req.model_dump(exclude_unset=True).items():
        setattr(cat, field, value)
    db.commit()
    db.refresh(cat)
    return success_response(data=CategoryOut.model_validate(cat).model_dump())


@router.delete("/categories/{category_id}", summary="删除分类")
def delete_category(category_id: int, db: Session = Depends(get_db)):
    cat = db.query(Category).filter(Category.id == category_id).first()
    if not cat:
        return error_response(404, "分类不存在")
    # 检查是否有图书使用此分类
    book_count = db.query(Book).filter(Book.category_id == category_id, Book.is_deleted == False).count()
    if book_count > 0:
        return error_response(400, f"该分类下还有{book_count}本图书，无法删除")
    db.delete(cat)
    db.commit()
    return success_response(message="删除成功")


# ── 图书 ──────────────────────────────────────────────

@router.get("/books", summary="获取图书列表")
def list_books(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    keyword: Optional[str] = None,
    category_id: Optional[int] = None,
    db: Session = Depends(get_db),
):
    q = db.query(Book).filter(Book.is_deleted == False)
    if keyword:
        like = f"%{keyword}%"
        q = q.filter(or_(Book.title.like(like), Book.author.like(like), Book.isbn.like(like)))
    if category_id:
        q = q.filter(Book.category_id == category_id)

    total = q.count()
    books = q.order_by(Book.id.desc()).offset((page - 1) * page_size).limit(page_size).all()

    return success_response(data={
        "total": total,
        "page": page,
        "page_size": page_size,
        "items": [BookListOut.model_validate(b).model_dump() for b in books],
    })


@router.post("/books", summary="新增图书")
def create_book(req: BookCreate, db: Session = Depends(get_db)):
    existing = db.query(Book).filter(Book.isbn == req.isbn, Book.is_deleted == False).first()
    if existing:
        return error_response(400, "该ISBN已存在")

    if req.category_id:
        cat = db.query(Category).filter(Category.id == req.category_id).first()
        if not cat:
            return error_response(400, "分类不存在")

    book = Book(
        title=req.title,
        author=req.author,
        isbn=req.isbn,
        publisher=req.publisher,
        category_id=req.category_id,
        cover_image=req.cover_image,
        description=req.description,
        total_copies=req.total_copies,
        available_copies=req.total_copies,
    )
    db.add(book)
    db.flush()

    for i in range(1, req.total_copies + 1):
        copy = BookCopy(
            book_id=book.id,
            copy_no=f"{req.isbn}-C{i:02d}",
            status="available",
        )
        db.add(copy)

    db.commit()
    db.refresh(book)
    return success_response(data=BookOut.model_validate(book).model_dump())


@router.get("/books/{book_id}", summary="获取图书详情")
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id, Book.is_deleted == False).first()
    if not book:
        return error_response(404, "图书不存在")
    return success_response(data=BookOut.model_validate(book).model_dump())


@router.put("/books/{book_id}", summary="修改图书")
def update_book(book_id: int, req: BookUpdate, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id, Book.is_deleted == False).first()
    if not book:
        return error_response(404, "图书不存在")

    if req.isbn and req.isbn != book.isbn:
        dup = db.query(Book).filter(Book.isbn == req.isbn, Book.is_deleted == False, Book.id != book_id).first()
        if dup:
            return error_response(400, "该ISBN已存在")

    for field, value in req.model_dump(exclude_unset=True).items():
        setattr(book, field, value)

    db.commit()
    db.refresh(book)
    return success_response(data=BookOut.model_validate(book).model_dump())


@router.delete("/books/{book_id}", summary="删除图书")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id, Book.is_deleted == False).first()
    if not book:
        return error_response(404, "图书不存在")

    borrowed = db.query(BookCopy).filter(
        BookCopy.book_id == book_id, BookCopy.status == "borrowed"
    ).count()
    if borrowed > 0:
        return error_response(400, "该图书有副本借出中，无法删除")

    book.is_deleted = True
    db.commit()
    return success_response(message="删除成功")
