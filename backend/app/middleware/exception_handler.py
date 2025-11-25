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
            # Always print to console first for debugging
            print(f"\n{'='*80}")
            print(f"EXCEPTION CAUGHT: {type(exc).__name__}")
            print(f"Message: {str(exc)}")
            print(f"Path: {request.method} {request.url.path}")
            print(f"Traceback:\n{traceback.format_exc()}")
            print(f"{'='*80}\n")

            # Get database session for logging
            db: Session = SessionLocal()

            try:
                # Extract user info if available
                user_id = None
                if hasattr(request.state, 'user'):
                    user_id = request.state.user.id

                # Log the exception to database
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
                print("✓ Exception logged to database")

            except Exception as log_error:
                # If logging fails, at least print it
                print(f"✗ FAILED TO LOG TO DATABASE: {str(log_error)}")
                print(f"  {traceback.format_exc()}")

            finally:
                db.close()

            # Map exceptions to HTTP status codes
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            detail = str(exc)

            if isinstance(exc, ValueError):
                # Validation errors -> 400 Bad Request
                status_code = status.HTTP_400_BAD_REQUEST
            elif isinstance(exc, PermissionError):
                # Permission denied -> 403 Forbidden
                status_code = status.HTTP_403_FORBIDDEN
            elif isinstance(exc, KeyError):
                # Not found -> 404 Not Found
                status_code = status.HTTP_404_NOT_FOUND
            elif "HTTPException" in type(exc).__name__:
                # FastAPI HTTPException
                status_code = getattr(exc, 'status_code', status.HTTP_500_INTERNAL_SERVER_ERROR)
                detail = getattr(exc, 'detail', str(exc))
            else:
                # All other exceptions -> 500 Internal Server Error
                detail = "Internal server error"

            return JSONResponse(
                status_code=status_code,
                content={"detail": detail}
            )
