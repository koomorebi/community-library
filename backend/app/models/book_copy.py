from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class BookCopy(Base):
    __tablename__ = "book_copies"

    id = Column(Integer, primary_key=True, autoincrement=True)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False, index=True)
    copy_no = Column(String(20), nullable=False)
    book_location = Column(String(50))
    status = Column(String(20), default="available", nullable=False, index=True)
    version = Column(Integer, default=1, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    book = relationship("Book", back_populates="copies")
