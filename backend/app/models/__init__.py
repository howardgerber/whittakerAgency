# Database models (SQLAlchemy ORM)
# Import all models to ensure relationships are properly resolved
from app.models.user import User
from app.models.quote_request import QuoteRequest
from app.models.claim import Claim
from app.models.audit_log import AuditLog
from app.models.contact_message import ContactMessage
from app.models.system_log import SystemLog
from app.models.team_member import TeamMember
from app.models.attachment import Attachment

__all__ = [
    "User",
    "QuoteRequest",
    "Claim",
    "AuditLog",
    "ContactMessage",
    "SystemLog",
    "TeamMember",
    "Attachment",
]
