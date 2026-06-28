from contextlib import asynccontextmanager

import bcrypt
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine, SessionLocal
from app.models.admin import Admin
from app.models.category import Category
from app.middleware.auth import auth_middleware
from app.middleware.error_handler import error_handler_middleware
from app.routers import auth, books, members, borrows, stats, stats_ranking, book_history, member_detail


def _init_default_data():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        if not db.query(Admin).first():
            password_hash = bcrypt.hashpw("admin123".encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
            db.add(Admin(username="admin", password_hash=password_hash, name="管理员"))

        if not db.query(Category).first():
            for i, name in enumerate(["文学", "科技", "历史", "教育", "艺术", "生活"]):
                db.add(Category(name=name, sort_order=i))

        db.commit()
    finally:
        db.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    _init_default_data()
    yield


app = FastAPI(title="社区图书馆借阅管理系统", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.middleware("http")(error_handler_middleware)
app.middleware("http")(auth_middleware)

app.include_router(auth.router)
app.include_router(books.router)
app.include_router(members.router)
app.include_router(borrows.router)
app.include_router(stats.router)
app.include_router(stats_ranking.router)
app.include_router(book_history.router)
app.include_router(member_detail.router)


@app.get("/")
def root():
    return {"message": "社区图书馆借阅管理系统 API v1"}
