from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ForeignKey, Date, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class Claim(Base):
    """
    Lightweight claim reporting system.
    NOT a full claim processing system - no PII, no financial tracking.
    Just basic incident info to help agents prepare for customer visits.
    """
    __tablename__ = "claims"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    category = Column(String(30), nullable=False, index=True)
    subcategory = Column(String(30), nullable=True, index=True)
    incident_date = Column(Date, nullable=False)
    incident_summary = Column(Text, nullable=False)  # Brief summary from form (250 chars max)
    claim_data = Column(JSON, nullable=False)  # Stores all dynamic fields by category/subcategory
    appointment_requested = Column(Date, nullable=True)  # Preferred appointment date
    contact_preference = Column(String(20), nullable=False, default="either")  # email, phone, either
    preferred_contact_time = Column(String(20), nullable=True)  # morning, afternoon, evening, anytime
    additional_notes = Column(Text, nullable=True)  # Optional customer notes
    status = Column(String(20), default="submitted", nullable=False, index=True)  # submitted, contacted, closed
    admin_notes = Column(Text, nullable=True)  # Internal notes from admin, not visible to customer
    contacted_at = Column(TIMESTAMP, nullable=True)  # When agent reached out
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp(), nullable=False, index=True)
    updated_at = Column(
        TIMESTAMP,
        server_default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
        nullable=False
    )

    # Relationships
    user = relationship("User", back_populates="claims")
