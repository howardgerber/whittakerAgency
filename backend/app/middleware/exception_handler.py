from fastapi import Request, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.services.system_log_service import SystemLogService
import traceback


class GlobalExceptionMiddleware(BaseHTTPMiddleware):
    """
    Global exception handler middleware
    Catches all exceptions and logs them to the SystemLog table
    """

    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except Exception as exc:
            # Get database session for logging
            db: Session = SessionLocal()

            try:
                # Extract user info if available
                user_id = None
                if hasattr(request.state, 'user'):
                    user_id = request.state.user.id

                # Log the exception
                await SystemLogService.log_exception(
                    db=db,
                    level="ERROR",
                    message=f"Unhandled exception: {str(exc)}",
                    exception_type=type(exc).__name__,
                    exception_message=str(exc),
                    stack_trace=traceback.format_exc(),
                    request_method=request.method,
                    request_path=str(request.url.path),
                    request_ip=request.client.host if request.client else None,
                    user_id=user_id
                )

            finally:
                db.close()

            # Return appropriate HTTP response
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            detail = "Internal server error"

            # Map specific exceptions to HTTP status codes
            if "HTTPException" in type(exc).__name__:
                status_code = getattr(exc, 'status_code', status.HTTP_500_INTERNAL_SERVER_ERROR)
                detail = getattr(exc, 'detail', detail)

            return JSONResponse(
                status_code=status_code,
                content={"detail": detail}
            )
