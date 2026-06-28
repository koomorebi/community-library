from fastapi import Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError


async def error_handler_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except IntegrityError as e:
        return JSONResponse(
            status_code=400,
            content={
                "code": 400,
                "message": "数据冲突，请检查输入是否重复",
                "detail": {"error": str(e.orig)},
            },
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "code": 500,
                "message": "系统繁忙，请稍后重试",
                "detail": {"error": str(e)},
            },
        )
