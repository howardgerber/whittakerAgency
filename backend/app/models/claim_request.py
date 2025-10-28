from sqlalchemy import Column, Integer, Text, Enum, TIMESTAMP, ForeignKey, Date
from sqlalchemy.sql import func
from app.core.database import Base
from app.models.quote_request import InsuranceType, RequestStatus


class ClaimRequest(Base):
    __tablename__ = "claim_requests"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    insurance_type = Column(Enum(InsuranceType), nullable=False)
    incident_description = Column(Text, nullable=False)
    incident_date = Column(Date, nullable=False)
    status = Column(Enum(RequestStatus), default=RequestStatus.PENDING, nullable=False, index=True)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp(), nullable=False, index=True)
    updated_at = Column(
        TIMESTAMP,
        server_default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
        nullable=False
    )
