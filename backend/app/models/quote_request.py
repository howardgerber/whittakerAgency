from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ForeignKey, JSON, Numeric, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class QuoteRequest(Base):
    __tablename__ = "quote_requests"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    category = Column(String(30), nullable=False, index=True)
    subcategory = Column(String(30), nullable=True, index=True)
    status = Column(String(30), default="pending", nullable=False, index=True)  # pending, in_review, quoted, accepted, declined
    quote_data = Column(JSON, nullable=False)
    agent_notes = Column(Text, nullable=True)
    customer_notes = Column(Text, nullable=True)
    quote_amount = Column(Numeric(10, 2), nullable=True)
    appointment_date = Column(Date, nullable=True)
    quoted_at = Column(TIMESTAMP, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp(), nullable=False, index=True)
    updated_at = Column(
        TIMESTAMP,
        server_default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
        nullable=False
    )

    # Relationships
    user = relationship("User", back_populates="quote_requests")
