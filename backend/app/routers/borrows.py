from datetime import datetime, date, timedelta, timezone

from fastapi import APIRouter, Depends, Query
from sqlalchemy import and_
from sqlalchemy.orm import Session

from app.config import BORROW_DAYS, MAX_RENEW_COUNT, UNDO_WINDOW_MINUTES
from app.database import get_db
from app.models.book import Book
from app.models.book_copy import BookCopy
from app.models.borrow import Borrow
from app.models.member import Member
from app.schemas.borrow import BorrowRequest, ReturnRequest, RenewRequest, BorrowOut, BorrowBookCopyInfo, BorrowBookInfo, BorrowMemberInfo
from app.schemas.common import success_response, error_response

router = APIRouter(prefix="/api/v1/borrows", tags=["借阅管理"])


def _borrow_to_dict(b: Borrow) -> dict:
    book_copy = b.book_copy
    book = book_copy.book if book_copy else None
    return BorrowOut(
        id=b.id,
        book_copy=BorrowBookCopyInfo.model_validate(book_copy) if book_copy else None,
        book=BorrowBookInfo(id=book.id, title=book.title, author=book.author) if book else None,
        member=BorrowMemberInfo.model_validate(b.member) if b.member else None,
        borrow_date=b.borrow_date,
        due_date=b.due_date,
        return_date=b.return_date,
        renew_count=b.renew_count,
        status=b.status,
        created_at=b.created_at,
    ).model_dump()


@router.post("/borrow", summary="借书")
def borrow_book(req: BorrowRequest, db: Session = Depends(get_db)):
    # 1. 验证会员
    member = db.query(Member).filter(Member.id == req.member_id, Member.is_deleted == False).first()
    if not member:
        return error_response(404, "未找到此会员")

    if member.status != "active":
        return error_response(403, "该会员账号已被冻结，无法借书")

    # 检查逾期
    overdue = db.query(Borrow).filter(
        Borrow.member_id == member.id,
        Borrow.status == "overdue",
    ).first()
    if overdue:
        return error_response(409, "该会员有逾期图书，请先归还再借新书")

    # 检查借阅上限
    active_borrows = db.query(Borrow).filter(
        Borrow.member_id == member.id,
        Borrow.status.in_(["borrowed", "overdue"]),
    ).count()
    if active_borrows >= member.max_borrows:
        return error_response(409, f"您已经借了{member.max_borrows}本书，先还一些再借新的吧")

    # 2. 根据book_id找到可用的BookCopy
    copy = db.query(BookCopy).filter(
        BookCopy.book_id == req.book_id,
        BookCopy.status == "available",
    ).with_for_update().first()
    if not copy:
        return error_response(404, "此书暂无可借副本")

    # 3 & 4. 乐观锁检查 + 更新
    expected_version = copy.version
    copy.status = "borrowed"
    copy.version = expected_version + 1

    # 5. 更新Book可借数
    book = db.query(Book).filter(Book.id == copy.book_id).first()
    if book.available_copies <= 0:
        db.rollback()
        return error_response(409, "库存数据异常，请刷新后重试")
    book.available_copies -= 1

    # 6. 插入Borrow记录
    now = datetime.now(timezone.utc)
    borrow = Borrow(
        book_copy_id=copy.id,
        member_id=member.id,
        operator_id=1,  # TODO: 从JWT中获取
        borrow_date=now,
        due_date=(now + timedelta(days=BORROW_DAYS)).date(),
        status="borrowed",
    )
    db.add(borrow)
    db.commit()
    db.refresh(borrow)

    return success_response(data=_borrow_to_dict(borrow), message="借书成功")


@router.post("/return", summary="还书")
def return_book(req: ReturnRequest, db: Session = Depends(get_db)):
    borrow = db.query(Borrow).filter(Borrow.id == req.borrow_id).first()
    if not borrow:
        return error_response(404, "未找到此借阅记录")

    if borrow.status == "returned":
        return error_response(400, "此书已归还")

    # 更新Borrow
    now = datetime.now(timezone.utc)
    borrow.return_date = now
    borrow.status = "returned"

    # 更新BookCopy
    copy = db.query(BookCopy).filter(BookCopy.id == borrow.book_copy_id).first()
    copy.status = "available"

    # 更新Book可借数
    book = db.query(Book).filter(Book.id == copy.book_id).first()
    book.available_copies += 1

    db.commit()
    db.refresh(borrow)

    return success_response(data=_borrow_to_dict(borrow), message="归还成功")


@router.post("/renew", summary="续借")
def renew_book(req: RenewRequest, db: Session = Depends(get_db)):
    borrow = db.query(Borrow).filter(Borrow.id == req.borrow_id).first()
    if not borrow:
        return error_response(404, "未找到此借阅记录")

    if borrow.status != "borrowed":
        return error_response(400, "只能续借借出中的图书")

    if borrow.renew_count >= MAX_RENEW_COUNT:
        return error_response(409, "每本书只能续借1次哦")

    borrow.due_date = borrow.due_date + timedelta(days=BORROW_DAYS)
    borrow.renew_count += 1

    db.commit()
    db.refresh(borrow)

    return success_response(data=_borrow_to_dict(borrow), message="续借成功")


@router.get("", summary="获取借阅记录")
def list_borrows(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    status: str = None,
    member_id: int = None,
    db: Session = Depends(get_db),
):
    from datetime import date
    today = date.today()

    # 先自动更新逾期状态
    overdue_borrows = db.query(Borrow).filter(
        Borrow.status == "borrowed",
        Borrow.due_date < today
    ).all()
    for b in overdue_borrows:
        b.status = "overdue"
    if overdue_borrows:
        db.commit()

    q = db.query(Borrow)

    # 支持 overdue 状态筛选
    if status == "overdue":
        q = q.filter(Borrow.status == "overdue")
    elif status:
        q = q.filter(Borrow.status == status)

    if member_id:
        q = q.filter(Borrow.member_id == member_id)

    total = q.count()
    borrows = q.order_by(Borrow.id.desc()).offset((page - 1) * page_size).limit(page_size).all()

    return success_response(data={
        "total": total,
        "page": page,
        "page_size": page_size,
        "items": [_borrow_to_dict(b) for b in borrows],
    })


@router.post("/undo/{borrow_id}", summary="撤销借阅")
def undo_borrow(borrow_id: int, db: Session = Depends(get_db)):
    borrow = db.query(Borrow).filter(Borrow.id == borrow_id).first()
    if not borrow:
        return error_response(404, "未找到此借阅记录")

    if borrow.status != "borrowed":
        return error_response(400, "只能撤销借出中的记录")

    now = datetime.now(timezone.utc)
    elapsed = (now - borrow.borrow_date.replace(tzinfo=timezone.utc)).total_seconds() / 60
    if elapsed > UNDO_WINDOW_MINUTES:
        return error_response(409, f"已超过{UNDO_WINDOW_MINUTES}分钟，无法撤销")

    # 回滚借书操作
    borrow.status = "returned"
    borrow.return_date = now

    copy = db.query(BookCopy).filter(BookCopy.id == borrow.book_copy_id).first()
    copy.status = "available"

    book = db.query(Book).filter(Book.id == copy.book_id).first()
    book.available_copies += 1

    db.commit()

    return success_response(message="撤销成功")
