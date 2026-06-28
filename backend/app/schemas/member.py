from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel


class MemberCreate(BaseModel):
    name: str
    phone: str
    email: Optional[str] = None
    id_card: Optional[str] = None
    address: Optional[str] = None
    max_borrows: int = 5


class MemberUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    id_card: Optional[str] = None
    address: Optional[str] = None
    status: Optional[str] = None
    max_borrows: Optional[int] = None


class MemberOut(BaseModel):
    id: int
    name: str
    phone: str
    email: Optional[str] = None
    id_card: Optional[str] = None
    card_no: str
    address: Optional[str] = None
    join_date: date
    status: str
    max_borrows: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
