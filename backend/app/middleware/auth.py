from datetime import datetime, timezone

import jwt
from fastapi import Request
from fastapi.responses import JSONResponse

from app.config import JWT_SECRET_KEY, JWT_ALGORITHM

EXEMPT_PATHS = {"/api/v1/auth/login", "/docs", "/openapi.json", "/redoc", "/"}


async def auth_middleware(request: Request, call_next):
    if request.method == "OPTIONS":
        return await call_next(request)

    path = request.url.path
    if path in EXEMPT_PATHS or path.startswith("/docs") or path.startswith("/openapi"):
        return await call_next(request)

    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return JSONResponse(
            status_code=401,
            content={"code": 401, "message": "未登录，请先登录", "detail": None},
        )

    token = auth_header.split(" ", 1)[1]
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        exp = payload.get("exp")
        if exp and datetime.fromtimestamp(exp, tz=timezone.utc) < datetime.now(timezone.utc):
            return JSONResponse(
                status_code=401,
                content={"code": 401, "message": "登录已过期，请重新登录", "detail": None},
            )
        request.state.user = payload
    except jwt.ExpiredSignatureError:
        return JSONResponse(
            status_code=401,
            content={"code": 401, "message": "登录已过期，请重新登录", "detail": None},
        )
    except jwt.InvalidTokenError:
        return JSONResponse(
            status_code=401,
            content={"code": 401, "message": "无效的登录凭证", "detail": None},
        )

    return await call_next(request)
