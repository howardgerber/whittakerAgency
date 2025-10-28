from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ForeignKey, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class ContactMessage(Base):
    """Contact messages from users (authenticated or guest)"""
    __tablename__ = "contact_messages"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    full_name = Column(String(200), nullable=False)
    email = Column(String(254), nullable=False)
    phone = Column(String(12), nullable=True)  # Format: XXX.XXX.XXXX
    subject = Column(String(50), nullable=False)  # general, quote, claim, policy, other, etc.
    message = Column(Text, nullable=False)
    status = Column(String(20), default="new", nullable=False, index=True)  # new, read, responded, closed
    admin_response = Column(Text, nullable=True)
    appointment_date = Column(Date, nullable=True)
    responded_at = Column(TIMESTAMP, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp(), nullable=False, index=True)
    updated_at = Column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp(), nullable=False)

    # Relationships
    user = relationship("User", back_populates="contact_messages")
