from datetime import datetime

from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(200), nullable=False, index=True)
    author = Column(String(100), nullable=False, index=True)
    isbn = Column(String(25), unique=True, nullable=False)
    publisher = Column(String(100))
    category_id = Column(Integer, ForeignKey("categories.id"))
    cover_image = Column(String(500))
    description = Column(Text)
    total_copies = Column(Integer, default=0, nullable=False)
    available_copies = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    is_deleted = Column(Boolean, default=False, nullable=False)

    category = relationship("Category", lazy="joined")
    copies = relationship("BookCopy", back_populates="book", lazy="selectin")
