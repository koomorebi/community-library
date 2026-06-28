from datetime import datetime, date

from sqlalchemy import Column, Integer, String, Date, Boolean, DateTime

from app.database import Base


class Member(Base):
    __tablename__ = "members"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, index=True)
    phone = Column(String(25), unique=True, nullable=False)
    id_card = Column(String(20))
    card_no = Column(String(20), unique=True, nullable=False)
    address = Column(String(200))
    email = Column(String(100))
    join_date = Column(Date, default=date.today, nullable=False)
    status = Column(String(20), default="active", nullable=False)
    max_borrows = Column(Integer, default=5, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    is_deleted = Column(Boolean, default=False, nullable=False)
