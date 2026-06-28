from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload

from app.database import get_db
from app.models.borrow import Borrow
from app.models.book import Book
from app.models.book_copy import BookCopy

router = APIRouter(prefix="/api/v1/books", tags=["图书"])


@router.get("/{book_id}/borrow-history", summary="获取图书借阅历史")
def get_book_borrow_history(
    book_id: int,
    db: Session = Depends(get_db),
):
    """获取某本书的借阅历史"""
    
    # 检查图书是否存在
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="图书不存在")
    
    # 查询该书所有借阅记录（通过 BookCopy 关联）
    borrows = (
        db.query(Borrow)
        .join(BookCopy, Borrow.book_copy_id == BookCopy.id)
        .filter(BookCopy.book_id == book_id)
        .options(joinedload(Borrow.member))
        .order_by(Borrow.borrow_date.desc())
        .all()
    )
    
    # 格式化结果
    history = []
    for borrow in borrows:
        history.append({
            "id": borrow.id,
            "borrow_date": borrow.borrow_date.isoformat() if borrow.borrow_date else None,
            "due_date": borrow.due_date.isoformat() if borrow.due_date else None,
            "return_date": borrow.return_date.isoformat() if borrow.return_date else None,
            "renew_count": borrow.renew_count,
            "status": borrow.status,
            "member_name": borrow.member.name if borrow.member else None,
            "member_card_no": borrow.member.card_no if borrow.member else None,
        })
    
    return {
        "code": 200,
        "message": "success",
        "data": {
            "book": {
                "id": book.id,
                "title": book.title,
                "author": book.author,
            },
            "total_borrows": len(history),
            "history": history,
        }
    }
