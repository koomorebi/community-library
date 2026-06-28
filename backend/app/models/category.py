from sqlalchemy import Column, Integer, String

from app.database import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True, nullable=False)
    sort_order = Column(Integer, default=0, nullable=False)
