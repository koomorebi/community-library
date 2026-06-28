from datetime import datetime, timedelta, timezone

import bcrypt
import jwt
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.config import JWT_SECRET_KEY, JWT_ALGORITHM, JWT_EXPIRE_HOURS
from app.database import get_db
from app.models.admin import Admin
from app.schemas.auth import LoginRequest, LoginResponse
from app.schemas.common import success_response, error_response

router = APIRouter(prefix="/api/v1/auth", tags=["认证"])


@router.post("/login", summary="管理员登录")
def login(req: LoginRequest, db: Session = Depends(get_db)):
    admin = db.query(Admin).filter(Admin.username == req.username).first()
    if not admin:
        return error_response(401, "用户名或密码错误")

    if not bcrypt.checkpw(req.password.encode("utf-8"), admin.password_hash.encode("utf-8")):
        return error_response(401, "用户名或密码错误")

    if not admin.is_active:
        return error_response(403, "账号已被禁用")

    expire = datetime.now(timezone.utc) + timedelta(hours=JWT_EXPIRE_HOURS)
    token = jwt.encode(
        {"sub": str(admin.id), "username": admin.username, "name": admin.name, "exp": expire},
        JWT_SECRET_KEY,
        algorithm=JWT_ALGORITHM,
    )

    return success_response(
        data=LoginResponse(access_token=token, name=admin.name).model_dump()
    )
