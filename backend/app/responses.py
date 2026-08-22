from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import Any

def success_response(data: Any, message: str = "Success", status_code: int = 200) -> JSONResponse:
    content = {
        "success": True,
        "message": message,
        "data": data
    }
    return JSONResponse(
        status_code=status_code,
        content=jsonable_encoder(content)
    )

def error_response(message: str, error_code: str, status_code: int = 400) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={
            "success": False,
            "error": message,
            "error_code": error_code,
            "data": None
        }
    )

def paginated_response(data: list[Any], total: int, limit: int, offset: int, message: str = "Success", status_code: int = 200) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={
            "success": True,
            "message": message,
            "data": data,
            "pagination": {
                "total": total,
                "limit": limit,
                "offset": offset
            }
        }
    )
