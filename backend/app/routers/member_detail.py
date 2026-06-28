from datetime import datetime, date

from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.member import Member
from app.models.borrow import Borrow
from app.models.book import Book
from app.models.book_copy import BookCopy
from app.schemas.common import success_response, error_response

router = APIRouter(prefix="/api/v1/members", tags=["会员详情"])


@router.get("/{member_id}/detail", summary="获取会员详情")
def get_member_detail(member_id: int, db: Session = Depends(get_db)):
    """获取会员详情，包含统计信息和借阅历史"""
    member = db.query(Member).filter(Member.id == member_id, Member.is_deleted == False).first()
    if not member:
        return error_response(404, "会员不存在")

    # 统计信息
    total_borrows = db.query(Borrow).filter(Borrow.member_id == member_id).count()
    current_borrows = db.query(Borrow).filter(
        Borrow.member_id == member_id,
        Borrow.status.in_(["borrowed", "overdue"])
    ).count()
    overdue_count = db.query(Borrow).filter(
        Borrow.member_id == member_id,
        Borrow.status == "overdue"
    ).count()

    # 借阅历史（最近20条）
    borrows = db.query(Borrow).filter(
        Borrow.member_id == member_id
    ).order_by(Borrow.borrow_date.desc()).limit(20).all()

    borrow_history = []
    for b in borrows:
        copy = db.query(BookCopy).filter(BookCopy.id == b.book_copy_id).first()
        book = db.query(Book).filter(Book.id == copy.book_id).first() if copy else None

        # 检查是否逾期（未归还且已过期）
        status = b.status
        if status == "borrowed" and b.due_date < date.today():
            status = "overdue"

        borrow_history.append({
            "id": b.id,
            "book_title": book.title if book else "未知",
            "book_author": book.author if book else "未知",
            "borrow_date": b.borrow_date.isoformat() if b.borrow_date else None,
            "due_date": b.due_date.isoformat() if b.due_date else None,
            "return_date": b.return_date.isoformat() if b.return_date else None,
            "renew_count": b.renew_count,
            "status": status,
        })

    return success_response(data={
        "member": {
            "id": member.id,
            "name": member.name,
            "phone": member.phone,
            "email": member.email,
            "id_card": member.id_card,
            "address": member.address,
            "card_no": member.card_no,
            "max_borrows": member.max_borrows,
            "status": member.status,
            "created_at": member.created_at.isoformat() if member.created_at else None,
        },
        "stats": {
            "total_borrows": total_borrows,
            "current_borrows": current_borrows,
            "overdue_count": overdue_count,
        },
        "borrow_history": borrow_history,
    })
