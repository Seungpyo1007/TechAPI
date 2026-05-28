"""Error types and handlers producing the §7.5 error envelope."""

from __future__ import annotations

import uuid

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

DOCS_BASE = "https://techapi.dev/docs/errors"

# HTTP status → (default error code, docs anchor)
_STATUS_CODE_MAP: dict[int, str] = {
    400: "INVALID_REQUEST",
    401: "UNAUTHORIZED",
    403: "FORBIDDEN",
    404: "NOT_FOUND",
    422: "VALIDATION_ERROR",
    429: "RATE_LIMIT_EXCEEDED",
    500: "INTERNAL_ERROR",
    503: "SERVICE_UNAVAILABLE",
}


class APIError(Exception):
    """Raised by routers to emit a structured error (§7.5)."""

    def __init__(self, status_code: int, code: str, message: str) -> None:
        self.status_code = status_code
        self.code = code
        self.message = message
        super().__init__(message)


def not_found(resource: str, slug: str) -> APIError:
    return APIError(
        status.HTTP_404_NOT_FOUND,
        "NOT_FOUND",
        f"{resource} with slug '{slug}' not found",
    )


def _request_id(request: Request) -> str:
    rid = getattr(request.state, "request_id", None)
    if isinstance(rid, str):
        return rid
    return f"req_{uuid.uuid4().hex[:16]}"


def _envelope(request: Request, status_code: int, code: str, message: str) -> JSONResponse:
    anchor = code.lower().replace("_", "-")
    return JSONResponse(
        status_code=status_code,
        content={
            "error": {
                "code": code,
                "message": message,
                "request_id": _request_id(request),
                "documentation_url": f"{DOCS_BASE}#{anchor}",
            }
        },
    )


def register_error_handlers(app: FastAPI) -> None:
    """Wire exception handlers so every error matches §7.5."""

    @app.exception_handler(APIError)
    async def _handle_api_error(request: Request, exc: APIError) -> JSONResponse:
        return _envelope(request, exc.status_code, exc.code, exc.message)

    @app.exception_handler(StarletteHTTPException)
    async def _handle_http_error(
        request: Request, exc: StarletteHTTPException
    ) -> JSONResponse:
        code = _STATUS_CODE_MAP.get(exc.status_code, "INTERNAL_ERROR")
        message = exc.detail if isinstance(exc.detail, str) else code
        return _envelope(request, exc.status_code, code, message)

    @app.exception_handler(RequestValidationError)
    async def _handle_validation_error(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        return _envelope(
            request,
            422,  # Unprocessable Content
            "VALIDATION_ERROR",
            "Request validation failed",
        )

    @app.exception_handler(Exception)
    async def _handle_unexpected(request: Request, exc: Exception) -> JSONResponse:
        return _envelope(
            request,
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "INTERNAL_ERROR",
            "An unexpected error occurred",
        )
