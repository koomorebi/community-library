from datetime import datetime

from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class Borrow(Base):
    __tablename__ = "borrows"

    id = Column(Integer, primary_key=True, autoincrement=True)
    book_copy_id = Column(Integer, ForeignKey("book_copies.id"), nullable=False, index=True)
    member_id = Column(Integer, ForeignKey("members.id"), nullable=False, index=True)
    operator_id = Column(Integer, ForeignKey("admins.id"), nullable=False)
    borrow_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    due_date = Column(Date, nullable=False, index=True)
    return_date = Column(DateTime)
    renew_count = Column(Integer, default=0, nullable=False)
    status = Column(String(20), default="borrowed", nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    book_copy = relationship("BookCopy", lazy="joined")
    member = relationship("Member", lazy="joined")
    operator = relationship("Admin", lazy="joined")
