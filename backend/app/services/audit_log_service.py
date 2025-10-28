from sqlalchemy.orm import Session
from app.models.audit_log import AuditLog
from typing import Optional


class AuditLogService:
    """Service for audit logging (user actions, data modifications)"""

    @staticmethod
    async def log_user_action(
        db: Session,
        user_id: Optional[int],
        action: str,
        entity_type: Optional[str] = None,
        entity_id: Optional[int] = None,
        details: Optional[str] = None,
        ip_address: Optional[str] = None
    ):
        """Log a user action to the audit_logs table"""
        audit_entry = AuditLog(
            user_id=user_id,
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            details=details,
            ip_address=ip_address
        )

        db.add(audit_entry)
        db.commit()
