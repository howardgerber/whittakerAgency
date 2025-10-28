from sqlalchemy import Column, Integer, String, Text, Enum, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base
import enum


class InsuranceType(str, enum.Enum):
    AUTO = "auto"
    HOME = "home"
    BUSINESS = "business"
    LIFE = "life"
    HEALTH = "health"
    MOTORCYCLE = "motorcycle"
    BOAT = "boat"
    RENTAL = "rental"


class RequestStatus(str, enum.Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class QuoteRequest(Base):
    __tablename__ = "quote_requests"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    insurance_type = Column(Enum(InsuranceType), nullable=False)
    coverage_details = Column(Text, nullable=True)
    status = Column(Enum(RequestStatus), default=RequestStatus.PENDING, nullable=False, index=True)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp(), nullable=False, index=True)
    updated_at = Column(
        TIMESTAMP,
        server_default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
        nullable=False
    )
