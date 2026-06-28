from typing import Any, Optional

from pydantic import BaseModel


class ResponseModel(BaseModel):
    code: int = 200
    message: str = "success"
    data: Any = None


class ErrorResponse(BaseModel):
    code: int
    message: str
    detail: Optional[Any] = None


def success_response(data: Any = None, message: str = "success") -> dict:
    return {"code": 200, "message": message, "data": data}


def error_response(code: int, message: str, detail: Any = None) -> dict:
    return {"code": code, "message": message, "detail": detail}
