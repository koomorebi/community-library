from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, extract
from sqlalchemy.orm import Session, joinedload

from app.database import get_db
from app.models.borrow import Borrow
from app.models.book import Book
from app.models.book_copy import BookCopy
from app.models.member import Member

router = APIRouter(prefix="/api/v1/stats", tags=["统计"])


@router.get("/ranking", summary="获取借阅排行榜")
def get_borrow_ranking(
    period: str = Query("all", description="统计周期: monthly, yearly, all"),
    year: Optional[int] = Query(None, description="年份"),
    month: Optional[int] = Query(None, description="月份"),
    limit: int = Query(20, description="返回数量"),
    db: Session = Depends(get_db),
):
    """获取图书借阅热度排行榜"""
    
    # 基础查询：通过 BookCopy 关联到 Book
    query = (
        db.query(
            Book.id,
            Book.title,
            Book.author,
            Book.isbn,
            Book.cover_image,
            func.count(Borrow.id).label("borrow_count"),
        )
        .join(BookCopy, Book.id == BookCopy.book_id)
        .join(Borrow, BookCopy.id == Borrow.book_copy_id)
    )
    
    # 根据周期筛选
    now = datetime.now()
    if period == "monthly":
        target_year = year or now.year
        target_month = month or now.month
        query = query.filter(
            extract("year", Borrow.borrow_date) == target_year,
            extract("month", Borrow.borrow_date) == target_month,
        )
    elif period == "yearly":
        target_year = year or now.year
        query = query.filter(
            extract("year", Borrow.borrow_date) == target_year
        )
    # period == "all" 不添加时间过滤
    
    # 分组、排序、限制
    results = (
        query.group_by(Book.id)
        .order_by(func.count(Borrow.id).desc())
        .limit(limit)
        .all()
    )
    
    # 格式化结果
    ranking = []
    for rank, item in enumerate(results, 1):
        ranking.append({
            "rank": rank,
            "book_id": item.id,
            "title": item.title,
            "author": item.author,
            "isbn": item.isbn,
            "cover_image": item.cover_image,
            "borrow_count": item.borrow_count,
        })
    
    # 构建周期描述
    if period == "monthly":
        period_label = f"{target_year}年{target_month}月"
    elif period == "yearly":
        period_label = f"{target_year}年"
    else:
        period_label = "全部时间"
    
    return {
        "code": 200,
        "message": "success",
        "data": {
            "period": period,
            "period_label": period_label,
            "ranking": ranking,
        }
    }
