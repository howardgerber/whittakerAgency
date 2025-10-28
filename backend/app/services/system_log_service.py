from sqlalchemy.orm import Session
from app.models.system_log import SystemLog, LogLevel
from typing import Optional


class SystemLogService:
    """Service for system logging (errors, exceptions, system events)"""

    @staticmethod
    async def log_exception(
        db: Session,
        level: str,
        message: str,
        exception_type: Optional[str] = None,
        exception_message: Optional[str] = None,
        stack_trace: Optional[str] = None,
        request_method: Optional[str] = None,
        request_path: Optional[str] = None,
        request_ip: Optional[str] = None,
        user_id: Optional[int] = None
    ):
        """Log an exception to the system_logs table"""
        log_entry = SystemLog(
            level=LogLevel[level],
            message=message,
            exception_type=exception_type,
            exception_message=exception_message,
            stack_trace=stack_trace,
            request_method=request_method,
            request_path=request_path,
            request_ip=request_ip,
            user_id=user_id
        )

        db.add(log_entry)
        db.commit()

    @staticmethod
    async def log_info(
        db: Session,
        message: str,
        user_id: Optional[int] = None
    ):
        """Log an informational message"""
        log_entry = SystemLog(
            level=LogLevel.INFO,
            message=message,
            user_id=user_id
        )

        db.add(log_entry)
        db.commit()
