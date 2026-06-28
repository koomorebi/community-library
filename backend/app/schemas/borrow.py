from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel


class BorrowRequest(BaseModel):
    member_id: int
    book_id: int


class ReturnRequest(BaseModel):
    borrow_id: int


class RenewRequest(BaseModel):
    borrow_id: int


class BorrowBookCopyInfo(BaseModel):
    id: int
    copy_no: str
    book_location: Optional[str] = None

    model_config = {"from_attributes": True}


class BorrowBookInfo(BaseModel):
    id: int
    title: str
    author: str

    model_config = {"from_attributes": True}


class BorrowMemberInfo(BaseModel):
    id: int
    name: str
    card_no: str

    model_config = {"from_attributes": True}


class BorrowOut(BaseModel):
    id: int
    book_copy: Optional[BorrowBookCopyInfo] = None
    book: Optional[BorrowBookInfo] = None
    member: Optional[BorrowMemberInfo] = None
    borrow_date: datetime
    due_date: date
    return_date: Optional[datetime] = None
    renew_count: int
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}
