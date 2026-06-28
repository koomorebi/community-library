import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./community_library.db")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "community-library-secret-key-change-in-production")
JWT_ALGORITHM = "HS256"
JWT_EXPIRE_HOURS = 24
BORROW_DAYS = 30
MAX_RENEW_COUNT = 1
UNDO_WINDOW_MINUTES = 5
