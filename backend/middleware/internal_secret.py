from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from core.config import settings

EXCLUDE_PATHS = {"/", "/health", "/docs"}

class InternalSecretMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path not in EXCLUDE_PATHS:
            secret = request.headers.get("x-internal-secret")
            if not secret or secret != settings.secret_key:
                return JSONResponse(
                    {"detail": "Unauthorized: invalid or missing internal secret"},
                    status_code=401
                )
        response = await call_next(request)
        return response
