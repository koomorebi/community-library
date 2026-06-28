from datetime import datetime, timezone, timedelta

from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.book import Book
from app.models.borrow import Borrow
from app.schemas.common import success_response

router = APIRouter(prefix="/api/v1/stats", tags=["统计"])


@router.get("", summary="获取统计数据")
def get_stats(db: Session = Depends(get_db)):
    total_books = db.query(func.sum(Book.total_copies)).filter(Book.is_deleted == False).scalar() or 0
    borrowed_count = db.query(Borrow).filter(Borrow.status == "borrowed").count()
    overdue_count = db.query(Borrow).filter(Borrow.status == "overdue").count()

    today_start = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    today_borrows = db.query(Borrow).filter(Borrow.borrow_date >= today_start).count()
    today_returns = db.query(Borrow).filter(
        Borrow.return_date >= today_start,
        Borrow.status == "returned",
    ).count()

    return success_response(data={
        "total_books": total_books,
        "borrowed_count": borrowed_count,
        "overdue_count": overdue_count,
        "today_borrows": today_borrows,
        "today_returns": today_returns,
    })
